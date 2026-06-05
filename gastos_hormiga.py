#!/usr/bin/env python3
# gastos_hormiga.py
import sqlite3
from datetime import datetime, date
import csv
import os
import sys

DB_FILE = os.path.join(os.path.expanduser("~"), ".gastos_hormiga.db")

def init_db(conn):
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        monto REAL NOT NULL,
        categoria TEXT NOT NULL,
        nota TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS config (
        clave TEXT PRIMARY KEY,
        valor TEXT
    )""")
    conn.commit()

def add_gasto(conn, monto, categoria, nota="", fecha=None):
    if fecha is None:
        fecha = datetime.now().isoformat()
    c = conn.cursor()
    c.execute("INSERT INTO gastos (fecha, monto, categoria, nota) VALUES (?, ?, ?, ?)",
              (fecha, monto, categoria, nota))
    conn.commit()
    print("Gasto registrado.")

def listar_gastos(conn, desde=None, hasta=None, categoria=None, limit=100):
    q = "SELECT id, fecha, monto, categoria, nota FROM gastos WHERE 1=1"
    params = []
    if desde:
        q += " AND date(fecha) >= date(?)"
        params.append(desde)
    if hasta:
        q += " AND date(fecha) <= date(?)"
        params.append(hasta)
    if categoria:
        q += " AND categoria = ?"
        params.append(categoria)
    q += " ORDER BY fecha DESC LIMIT ?"
    params.append(limit)
    c = conn.cursor()
    for row in c.execute(q, params):
        print(f"{row[0]:>3} | {row[1][:19]} | ${row[2]:.2f} | {row[3]} | {row[4]}")

def resumen_mes(conn, year=None, month=None):
    if year is None or month is None:
        today = date.today()
        year, month = today.year, today.month
    start = f"{year:04d}-{month:02d}-01"
    c = conn.cursor()
    c.execute("SELECT SUM(monto) FROM gastos WHERE date(fecha) >= date(?) AND date(fecha) < date(?, '+1 month')", (start, start))
    total = c.fetchone()[0] or 0.0
    print(f"Resumen {year}-{month:02d}: Total gastado = ${total:.2f}")
    c.execute("SELECT categoria, SUM(monto) FROM gastos WHERE date(fecha) >= date(?) AND date(fecha) < date(?, '+1 month') GROUP BY categoria ORDER BY SUM(monto) DESC", (start, start))
    print("Por categoría:")
    for cat, s in c.fetchall():
        print(f"  - {cat}: ${s:.2f}")
    # presupuesto
    c.execute("SELECT valor FROM config WHERE clave = 'presupuesto_mensual'")
    row = c.fetchone()
    if row:
        presupuesto = float(row[0])
        print(f"Presupuesto mensual: ${presupuesto:.2f}")
        if total > presupuesto:
            print("** Alerta: has superado el presupuesto mensual **")
        else:
            restante = presupuesto - total
            print(f"Restante: ${restante:.2f}")

def exportar_csv(conn, ruta):
    c = conn.cursor()
    c.execute("SELECT id, fecha, monto, categoria, nota FROM gastos ORDER BY fecha")
    rows = c.fetchall()
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "fecha", "monto", "categoria", "nota"])
        writer.writerows(rows)
    print(f"Exportado a {ruta}")

def set_presupuesto(conn, monto):
    c = conn.cursor()
    c.execute("INSERT INTO config (clave, valor) VALUES ('presupuesto_mensual', ?) ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor", (str(monto),))
    conn.commit()
    print("Presupuesto mensual guardado.")

def ayuda():
    print("""
Comandos disponibles:
  1  Registrar gasto
  2  Listar gastos
  3  Resumen mes actual
  4  Exportar a CSV
  5  Establecer presupuesto mensual
  6  Salir
""")

def menu_interactivo(conn):
    while True:
        ayuda()
        opt = input("Elige una opción (1-6): ").strip()
        if opt == "1":
            try:
                monto = float(input("Monto (ej. 12.50): ").strip())
            except ValueError:
                print("Monto inválido.")
                continue
            categoria = input("Categoría (ej. café, transporte): ").strip() or "varios"
            nota = input("Nota (opcional): ").strip()
            add_gasto(conn, monto, categoria, nota)
        elif opt == "2":
            desde = input("Desde (YYYY-MM-DD) dejar vacío para no filtrar: ").strip() or None
            hasta = input("Hasta (YYYY-MM-DD) dejar vacío para no filtrar: ").strip() or None
            categoria = input("Categoría filtrar dejar vacío para no filtrar: ").strip() or None
            listar_gastos(conn, desde, hasta, categoria, limit=500)
        elif opt == "3":
            ym = input("Mes y año (YYYY-MM) dejar vacío para mes actual: ").strip()
            if ym:
                try:
                    y, m = ym.split("-")
                    resumen_mes(conn, int(y), int(m))
                except Exception:
                    print("Formato inválido.")
            else:
                resumen_mes(conn)
        elif opt == "4":
            ruta = input("Ruta archivo CSV (ej. gastos.csv): ").strip() or "gastos_export.csv"
            exportar_csv(conn, ruta)
        elif opt == "5":
            try:
                monto = float(input("Presupuesto mensual ($): ").strip())
                set_presupuesto(conn, monto)
            except ValueError:
                print("Monto inválido.")
        elif opt == "6":
            print("Adiós.")
            break
        else:
            print("Opción no válida.")

def main():
    conn = sqlite3.connect(DB_FILE)
    init_db(conn)
    # Si se pasan argumentos, permitir acciones rápidas
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "add":
            # ejemplo: python gastos_hormiga.py add 3.5 cafe "café con leche"
            try:
                monto = float(sys.argv[2])
                categoria = sys.argv[3]
                nota = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
                add_gasto(conn, monto, categoria, nota)
            except Exception as e:
                print("Uso: gastos_hormiga.py add <monto> <categoria> [nota]")
        elif cmd == "export":
            ruta = sys.argv[2] if len(sys.argv) > 2 else "gastos_export.csv"
            exportar_csv(conn, ruta)
        elif cmd == "summary":
            resumen_mes(conn)
        else:
            print("Comando no reconocido.")
    else:
        menu_interactivo(conn)
    conn.close()

if __name__ == "__main__":
    main()

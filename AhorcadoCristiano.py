import random

# Lista de canciones cristianas (solo títulos, no letras completas)
canciones = [
    "Mi universo",                # Jesús Adrián Romero
    "Sumérgeme",                  # Jesús Adrián Romero
    "Rendir mi vida",             # Ericson Alexander Molano
    "El Vive Hoy",                # Ericson Alexander Molano
    "Abba Padre",                 # Fernel Monroy
    "Tu fidelidad",               # Juan Carlos Alvarado
    "Cristo no está muerto",      # Juan Carlos Alvarado
    "Ven Espíritu Santo",         # Fernel Monroy
    "Te daré lo mejor",           # Jesús Adrián Romero
    "Digno de alabar"             # Juan Carlos Alvarado
]

def elegir_palabra():
    return random.choice(canciones).upper()

def mostrar_tablero(palabra, letras_adivinadas):
    return " ".join([letra if letra in letras_adivinadas else "_" for letra in palabra])

def ahorcado():
    palabra = elegir_palabra()
    letras_adivinadas = set()
    intentos = 6
    usadas = set()

    print("🎵 Bienvenido al juego del Ahorcado 🎵")
    print("Tema: Canciones cristianas")
    print("Tienes", intentos, "intentos para adivinar la canción.")
    print(mostrar_tablero(palabra, letras_adivinadas))

    while intentos > 0:
        letra = input("Ingresa una letra: ").upper()

        if not letra.isalpha() or len(letra) != 1:
            print("Por favor ingresa solo una letra.")
            continue

        if letra in usadas:
            print("Ya usaste esa letra.")
            continue

        usadas.add(letra)

        if letra in palabra:
            letras_adivinadas.add(letra)
            print("¡Bien! La letra está en la palabra.")
        else:
            intentos -= 1
            print("Fallaste. Te quedan", intentos, "intentos.")

        tablero = mostrar_tablero(palabra, letras_adivinadas)
        print(tablero)

        if "_" not in tablero:
            print("🎉 ¡Felicidades! Has adivinado la canción:", palabra)
            break
    else:
        print("😢 Te quedaste sin intentos. La canción era:", palabra)

if __name__ == "__main__":
    ahorcado()

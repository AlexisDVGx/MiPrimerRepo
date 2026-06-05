# Ejemplo de documentación de comandos de GitHub CLI
## Comandos básicos de 'gh'

| Comando | Descripción |
|---|---|
| `gh auth login` | Permite iniciar sesi´on en GitHub desde la terminal. |
| `gh repo clone` | Clona un repositorio alojado en GitHub. |
| `gh issue list` | Muestra las incidencias disponibles en un repositorio. |
## Ejemplos de uso
### Iniciar sesión en GitHub
El código utilizado para iniciar sesión en GitHub fue el siguiente:
```bash
gh auth login
```
Este comando inicia el proceso de autenticaci´on en GitHub utilizando navegador web, token o SSH.--
### Clonar un repositorio
El siguiente comando permite clonar un repositorio remoto:
```bash
gh repo clone usuario/repositorio
```
Permite descargar un repositorio alojado en GitHub a la computadora local.--
### Listar incidencias
El siguiente comando muestra las incidencias abiertas del repositorio actual:
```bash
gh issue list
```
Muestra las incidencias abiertas asociadas al repositorio actual.
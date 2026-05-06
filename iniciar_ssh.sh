#!/bin/bash
echo "Iniciando agente SSH..."
eval "$(ssh-agent -s)"
echo "Agregando clave SSH..."
ssh-add ~/.ssh/id_ed25519
echo "Proceso Terminado."


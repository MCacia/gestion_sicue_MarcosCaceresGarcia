#!/bin/bash

# Definir las carpetas y los permisos
declare -A carpetas=(
    ["./gestionsicue103/src/db"]="755"
)

# Cambiar permisos
echo "Cambiando permisos..."
for carpeta in "${!carpetas[@]}"; do
    if [ -d "$carpeta" ]; then
        chmod "${carpetas[$carpeta]}" "$carpeta"
        echo "Permisos de $carpeta cambiados a ${carpetas[$carpeta]}"
    else
        echo "Advertencia: La carpeta $carpeta no existe"
    fi
done

echo "Proceso completado."
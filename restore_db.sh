#!/bin/bash

# Script para restaurar un respaldo de la base de datos
# Uso: ./restore_db.sh <archivo_respaldo>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_FILE="${SCRIPT_DIR}/data/calendar.db"
BACKUP_DIR="${SCRIPT_DIR}/data/backups"

# Verificar que se proporcionó un archivo de respaldo
if [ $# -eq 0 ]; then
    echo "❌ Error: Debe especificar un archivo de respaldo"
    echo ""
    echo "Uso: $0 <archivo_respaldo>"
    echo ""
    echo "📋 Respaldos disponibles:"
    if [ -d "${BACKUP_DIR}" ]; then
        ls -1t "${BACKUP_DIR}"/calendar_*.db 2>/dev/null | while read backup; do
            SIZE=$(du -h "$backup" | cut -f1)
            echo "   $(basename "$backup") (${SIZE})"
        done
    else
        echo "   No hay respaldos disponibles"
    fi
    exit 1
fi

BACKUP_SOURCE="$1"

# Si no es una ruta absoluta, buscar en el directorio de backups
if [[ ! "$BACKUP_SOURCE" = /* ]]; then
    BACKUP_SOURCE="${BACKUP_DIR}/${BACKUP_SOURCE}"
fi

# Verificar que existe el archivo de respaldo
if [ ! -f "${BACKUP_SOURCE}" ]; then
    echo "❌ Error: No se encuentra el archivo de respaldo: ${BACKUP_SOURCE}"
    exit 1
fi

# Crear un backup de la BD actual antes de restaurar
if [ -f "${DB_FILE}" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SAFETY_BACKUP="${BACKUP_DIR}/before_restore_${TIMESTAMP}.db"
    echo "🔒 Creando respaldo de seguridad de la BD actual..."
    cp "${DB_FILE}" "${SAFETY_BACKUP}"
    echo "   Guardado en: ${SAFETY_BACKUP}"
fi

# Restaurar el respaldo
echo ""
echo "♻️  Restaurando base de datos desde: $(basename ${BACKUP_SOURCE})"
cp "${BACKUP_SOURCE}" "${DB_FILE}"

if [ $? -eq 0 ]; then
    echo "✅ Base de datos restaurada exitosamente"
    echo ""
    echo "⚠️  Recuerda reiniciar la aplicación si está en ejecución:"
    echo "   sudo systemctl restart mycalendar.service"
else
    echo "❌ Error al restaurar la base de datos"
    if [ -f "${SAFETY_BACKUP}" ]; then
        echo ""
        echo "🔙 Puedes recuperar la BD anterior desde: ${SAFETY_BACKUP}"
    fi
    exit 1
fi

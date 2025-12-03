#!/bin/bash

# Script para respaldar la base de datos del calendario
# Uso: ./backup_db.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_FILE="${SCRIPT_DIR}/data/calendar.db"
BACKUP_DIR="${SCRIPT_DIR}/data/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/calendar_${TIMESTAMP}.db"

# Crear directorio de backups si no existe
mkdir -p "${BACKUP_DIR}"

# Verificar que existe la base de datos
if [ ! -f "${DB_FILE}" ]; then
    echo "❌ Error: No se encuentra la base de datos en ${DB_FILE}"
    exit 1
fi

# Realizar el backup
echo "📦 Creando respaldo de la base de datos..."
cp "${DB_FILE}" "${BACKUP_FILE}"

if [ $? -eq 0 ]; then
    echo "✅ Respaldo creado exitosamente: ${BACKUP_FILE}"
    
    # Mostrar tamaño del backup
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "   Tamaño: ${SIZE}"
    
    # Listar backups existentes
    echo ""
    echo "📋 Respaldos disponibles:"
    ls -lh "${BACKUP_DIR}" | grep "calendar_" | awk '{print "   " $9 " (" $5 ")"}'
    
    # Opcional: mantener solo los últimos 10 backups
    BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/calendar_*.db 2>/dev/null | wc -l)
    if [ ${BACKUP_COUNT} -gt 10 ]; then
        echo ""
        echo "🧹 Limpiando backups antiguos (manteniendo últimos 10)..."
        ls -t "${BACKUP_DIR}"/calendar_*.db | tail -n +11 | xargs rm -f
        echo "   Limpieza completada"
    fi
else
    echo "❌ Error al crear el respaldo"
    exit 1
fi

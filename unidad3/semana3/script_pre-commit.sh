#!/usr/bin/env bash
# .git/hooks/pre-commit
# Script de blindaje local de calidad previa al commit

set -e

echo "========================================================"
echo "Iniciando cadena de custodia local (Pre-commit Hook)..."
echo "========================================================"

# 1. Control Estetico Automatizado (Formatter)
echo "[Paso 1/3] Ejecutando Formatter (Black)..."
if ! black --check --diff src/ tests/; then
    echo ""
    echo "[FALLO CRITICO]: Inconsistencias de formato detectadas."
    echo "Ejecute 'black src/ tests/' para normalizar el estilo antes de commitear."
    exit 1
fi
echo "[OK] Formato estetico homogeneo verificado."
echo "--------------------------------------------------------"

# 2. Analisis Sintactico y Malas Practicas (Linter)
echo "[Paso 2/3] Ejecutando Linter (Flake8)..."
if ! flake8 src/ tests/ --count --max-complexity=10 --max-line-length=88 --statistics; then
    echo ""
    echo "[FALLO CRITICO]: Violaciones de reglas sintacticas o de estilo."
    echo "Corrija los errores reportados por Flake8 antes de continuar."
    exit 1
fi
echo "[OK] Analisis sintactico y estatico superado sin advertencias."
echo "--------------------------------------------------------"

# 3. Validacion Dinamica Local (Suite de Pruebas Unitarias)
echo "[Paso 3/3] Ejecutando Suite de Pruebas Unitarias (Pytest)..."
if ! pytest tests/ -q --disable-warnings; then
    echo ""
    echo "[FALLO CRITICO]: Pruebas unitarias fallidas detectadas."
    echo "Resuelva las aseveraciones en rojo antes de registrar cambios."
    exit 1
fi
echo "[OK] Suite de pruebas unitarias ejecutada exitosamente en verde."
echo "========================================================"
echo "Blindaje completado: Codigo apto para confirmacion local."
echo "========================================================"

exit 0

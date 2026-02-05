#!/bin/bash
# Script para instalar dependencias y ejecutar tests
# Mergington High School - QA Testing Suite

echo "=================================================="
echo "🔧 INSTALACIÓN DE DEPENDENCIAS"
echo "=================================================="
echo ""

cd /home/alberto/DataX/skills-getting-started-with-github-copilot

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"
echo ""

# Método 1: Intentar con venv (recomendado)
echo "📦 Método 1: Creando entorno virtual..."
if python3 -m venv venv 2>/dev/null; then
    echo "✅ Entorno virtual creado"
    source venv/bin/activate
    
    echo "📥 Instalando dependencias en venv..."
    if pip install -r requirements.txt; then
        echo "✅ Dependencias instaladas en venv"
        
        echo ""
        echo "=================================================="
        echo "🧪 EJECUTANDO TESTS"
        echo "=================================================="
        echo ""
        
        # Ejecutar script de validación rápida
        echo "1️⃣  Tests de validación rápida:"
        python quick_test.py
        
        echo ""
        echo "2️⃣  Tests completos con pytest:"
        pytest tests/test_app.py -v
        
        deactivate
        exit 0
    fi
fi

# Método 2: Intentar instalación de pip
echo ""
echo "⚠️  Método 1 falló. Intentando instalar pip..."
echo "Ejecuta: sudo apt update && sudo apt install python3-pip python3-venv"
echo ""
echo "Después de instalar pip, ejecuta:"
echo "  python3 -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  pytest tests/test_app.py -v"
echo ""

exit 1

#!/bin/bash

set -e

echo "================================================"
echo "🧪 Iniciando Suite de Testes Django"
echo "================================================"
echo ""

cd "$(dirname "$0")/../app"

echo "📁 Diretório atual: $(pwd)"
echo ""

if [ ! -f "manage.py" ]; then
    echo "❌ Erro: manage.py não encontrado!"
    exit 1
fi

echo "🧪 Rodando testes da aplicação 'core'..."
echo ""

python manage.py test core -v 2

echo ""
echo "================================================"
echo "  Testes Concluídos ✅"
echo "================================================"

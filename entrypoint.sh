#!/bin/bash

echo ""
echo "============================================"
echo "  Executando testes automatizados..."
echo "============================================"
echo ""

pytest test_api.py -v

echo ""
echo "============================================"
echo "  Iniciando a API..."
echo "============================================"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000

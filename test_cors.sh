#!/bin/bash

# Script para verificar que los headers CORS se envíen correctamente

API_URL="${1:-http://localhost:5000}"

echo "🔍 Verificando headers CORS en: $API_URL"
echo "================================================"

# Test 1: OPTIONS request (preflight)
echo -e "\n📋 TEST 1: Preflight request (OPTIONS)"
echo "---"
curl -i -X OPTIONS "$API_URL/products" \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type, Authorization" 2>/dev/null | grep -i "access-control"

# Test 2: GET request
echo -e "\n\n📋 TEST 2: GET request"
echo "---"
curl -i -X GET "$API_URL/products" \
  -H "Origin: http://localhost:3000" 2>/dev/null | grep -i "access-control"

# Test 3: POST request
echo -e "\n\n📋 TEST 3: POST request"
echo "---"
curl -i -X POST "$API_URL/products" \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" 2>/dev/null | grep -i "access-control"

echo -e "\n\n✅ Headers esperados:"
echo "   - Access-Control-Allow-Origin: *"
echo "   - Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS"
echo "   - Access-Control-Allow-Headers: Content-Type, Authorization"
echo "   - Access-Control-Expose-Headers: Content-Type, Authorization"
echo "   - Access-Control-Max-Age: 3600"

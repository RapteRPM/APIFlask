# 🌐 Configuración de CORS

## Resumen
La API ahora permite peticiones desde **diferentes dominios** de forma flexible y segura.

## Comportamiento Actual

### 📱 Desarrollo (`FLASK_ENV=development`)
```
Origen permitido: *
- Permite peticiones desde CUALQUIER dominio
- Ideal para desarrollo local y testing
```

### 🔒 Producción (`FLASK_ENV=production`)
```
Orígenes permitidos:
- * (cualquier dominio)
- http://localhost:3000
- http://localhost:5000
- http://localhost:8080
- http://127.0.0.1:3000
- http://127.0.0.1:5000
- http://127.0.0.1:8080
```

## Métodos HTTP Permitidos
- GET
- POST
- PUT
- DELETE
- PATCH
- OPTIONS

## Headers Permitidos
- Content-Type
- Authorization (para JWT)
- Cualquier otro header

## Configuración
- **Archivo**: `config/cors.py`
- **Usado en**: `main.py` (función `configure_cors()`)

## Para Personalizar CORS

Edita `config/cors.py` y modifica la lista `origins`:

```python
# Ejemplo: permitir solo dominios específicos
cors_config = {
    "origins": [
        "https://tupagina.com",
        "https://app.tupagina.com",
        "http://localhost:3000"
    ],
    ...
}
```

## Testing de CORS

Desde JavaScript:
```javascript
fetch('https://tu-api.railway.app/products', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer TU_TOKEN_JWT'
  }
})
.then(res => res.json())
.then(data => console.log(data))
```

Desde curl:
```bash
curl -X GET https://tu-api.railway.app/products \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -H "Content-Type: application/json"
```

## Notas Importantes

⚠️ **En Producción**: Se mantiene CORS abierto para máxima compatibilidad. Para mayor seguridad, edita `config/cors.py` y especifica solo los dominios permitidos.

✅ **Logs Reducidos**: La verbosidad de SQLAlchemy se ha reducido significativamente para una salida más limpia.

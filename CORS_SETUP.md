# 🔗 CONFIGURACIÓN CORS PARA FRONTEND

## ✅ CORS Ya Configurado

Tu backend **YA TIENE CORS CONFIGURADO** correctamente. La configuración actual permite:

- ✅ **Todos los orígenes** (`*`) - perfecto para desarrollo
- ✅ **Métodos HTTP**: GET, POST, PUT, DELETE, OPTIONS
- ✅ **Headers permitidos**: Content-Type, Authorization
- ✅ **Credenciales**: Habilitadas

## 🚀 Cómo Conectar tu Frontend

### 1. **Usar el archivo de integración**
Copia el contenido de `frontend_integration.js` a tu proyecto frontend.

### 2. **En tu HTML** (ejemplo para tu dashb.html):

```html
<!-- Agregar al final de tu archivo HTML, antes de </body> -->
<script src="frontend_integration.js"></script>
<script>
    // Ejemplo: Cargar productos al iniciar la página
    document.addEventListener('DOMContentLoaded', async () => {
        try {
            // Primero verificar conexión
            const conexionOK = await verificarConexionAPI();
            
            if (conexionOK) {
                // Tu backend está listo, aquí puedes cargar datos reales
                console.log('✅ Backend conectado exitosamente');
                
                // Ejemplo: reemplazar tu array estático con datos reales
                // const productosReales = await obtenerProductos();
                // renderProductos(productosReales);
            }
        } catch (error) {
            console.error('Error conectando con backend:', error);
        }
    });
</script>
```

### 3. **Modificar tu JavaScript existente** (en dashb.html):

```javascript
// ANTES (datos estáticos)
let productos = [];

// DESPUÉS (datos desde API)
let productos = [];

// Nueva función para cargar productos desde API
async function cargarProductosDesdeAPI() {
    try {
        // Necesitas estar logueado primero
        await iniciarSesion('tu_usuario', 'tu_password');
        
        // Cargar productos reales
        productos = await obtenerProductos();
        renderProductos();
    } catch (error) {
        console.error('Error cargando productos:', error);
        // Fallback a datos estáticos si falla
        productos = [];
    }
}

// Modificar guardarProducto para usar API
async function guardarProducto() {
    const nombre = document.getElementById("prodNombre").value;

    try {
        if (editIndex !== null) {
            // Actualizar producto existente
            const productoActualizado = await actualizarProducto(
                productos[editIndex].id, 
                nombre, 
                productos[editIndex].inventario, 
                productos[editIndex].categoria_id
            );
            productos[editIndex] = productoActualizado;
        } else {
            // Crear nuevo producto
            const nuevoProducto = await crearProducto(nombre, 0, 1); // categoria_id = 1 por defecto
            productos.push(nuevoProducto);
        }
        
        cancelarForm();
        renderProductos();
    } catch (error) {
        console.error('Error guardando producto:', error);
        alert('Error guardando el producto');
    }
}

// Modificar eliminarProducto para usar API
async function eliminarProducto(index) {
    try {
        await eliminarProducto(productos[index].id);
        productos.splice(index, 1);
        renderProductos();
    } catch (error) {
        console.error('Error eliminando producto:', error);
        alert('Error eliminando el producto');
    }
}
```

## 🔧 URLs de la API

| Servidor | URL | Uso |
|----------|-----|-----|
| **Desarrollo** | `http://127.0.0.1:5000` | Cuando ejecutas `python main.py` |
| **Codespaces** | `http://10.0.2.227:5000` | Si usas GitHub Codespaces |
| **Producción** | `https://tu-dominio.com` | Cuando despliegues |

## 🧪 Probar la Conexión

### Opción 1: Desde la consola del navegador
```javascript
// Abre la consola del navegador (F12) y ejecuta:
verificarConexionAPI().then(result => {
    console.log('Conexión:', result ? 'OK' : 'FALLÓ');
});
```

### Opción 2: Desde terminal (curl)
```bash
# Probar endpoint de salud
curl -X GET http://127.0.0.1:5000/api/health \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json"

# Respuesta esperada:
# {"status": "healthy", "timestamp": "2025-11-14", "version": "1.0", "cors": "enabled"}
```

## 🔐 Flujo de Autenticación

1. **Registrar usuario** (solo una vez):
```javascript
await registrarUsuario('mi_usuario', 'mi_password');
```

2. **Iniciar sesión**:
```javascript
await iniciarSesion('mi_usuario', 'mi_password');
// El token se guarda automáticamente
```

3. **Usar la API**:
```javascript
const productos = await obtenerProductos();
const categorias = await obtenerCategorias();
```

## 🚨 Solución de Problemas

### Error: "CORS blocked"
- ✅ **Ya resuelto** - tu backend tiene CORS configurado

### Error: "Failed to fetch"
- 🔍 **Verificar**: ¿El backend está ejecutándose?
- 🔍 **Verificar**: ¿La URL es correcta?

### Error: "401 Unauthorized"
- 🔐 **Solución**: Necesitas hacer login primero

### Error: "500 Internal Server Error"
- 🐛 **Revisar**: Los logs del servidor para detalles

## 📝 Ejemplo Completo Mínimo

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test API</title>
</head>
<body>
    <button onclick="testAPI()">Probar API</button>
    <div id="result"></div>

    <script src="frontend_integration.js"></script>
    <script>
        async function testAPI() {
            try {
                const conexion = await verificarConexionAPI();
                document.getElementById('result').innerHTML = 
                    conexion ? '✅ API Conectada' : '❌ API No Disponible';
            } catch (error) {
                document.getElementById('result').innerHTML = '❌ Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
```

## 🎯 Próximos Pasos

1. **Copiar** `frontend_integration.js` a tu proyecto
2. **Modificar** tu JavaScript para usar las funciones de API
3. **Probar** la conexión
4. **Implementar** autenticación en tu frontend
5. **Reemplazar** datos estáticos con datos reales de la API

¡Tu backend está **100% listo** para conectar con cualquier frontend! 🚀
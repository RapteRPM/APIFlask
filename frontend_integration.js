/**
 * GUÍA DE INTEGRACIÓN FRONTEND - API
 * 
 * Usa este código en tu frontend para conectarte a la API.
 * Tu backend ya está configurado con CORS apropiado.
 */

// Configuración de la API
const API_CONFIG = {
    baseURL: 'http://127.0.0.1:5000', // Cambia por tu URL de producción
    headers: {
        'Content-Type': 'application/json',
    }
};

// Token de autenticación (se guarda después del login)
let authToken = localStorage.getItem('authToken') || null;

// Función para realizar peticiones HTTP con manejo de CORS
async function apiRequest(endpoint, options = {}) {
    const url = `${API_CONFIG.baseURL}${endpoint}`;
    
    const defaultHeaders = { ...API_CONFIG.headers };
    
    // Agregar token de autorización si existe
    if (authToken) {
        defaultHeaders['Authorization'] = `Bearer ${authToken}`;
    }
    
    const requestOptions = {
        headers: defaultHeaders,
        ...options,
        headers: { ...defaultHeaders, ...options.headers }
    };
    
    try {
        const response = await fetch(url, requestOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// === FUNCIONES DE AUTENTICACIÓN ===

// Registrar usuario
async function registrarUsuario(username, password) {
    try {
        const response = await apiRequest('/registry', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        console.log('Usuario registrado:', response);
        return response;
    } catch (error) {
        console.error('Error registrando usuario:', error);
        throw error;
    }
}

// Iniciar sesión
async function iniciarSesion(username, password) {
    try {
        const response = await apiRequest('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        if (response.access_token) {
            authToken = response.access_token;
            localStorage.setItem('authToken', authToken);
            console.log('Sesión iniciada exitosamente');
        }
        
        return response;
    } catch (error) {
        console.error('Error iniciando sesión:', error);
        throw error;
    }
}

// Cerrar sesión
function cerrarSesion() {
    authToken = null;
    localStorage.removeItem('authToken');
    console.log('Sesión cerrada');
}

// === FUNCIONES DE PRODUCTOS ===

// Obtener todos los productos
async function obtenerProductos() {
    try {
        const productos = await apiRequest('/products', {
            method: 'GET'
        });
        
        console.log('Productos obtenidos:', productos);
        return productos;
    } catch (error) {
        console.error('Error obteniendo productos:', error);
        throw error;
    }
}

// Crear producto
async function crearProducto(nombre, inventario, categoria_id) {
    try {
        const nuevoProducto = await apiRequest('/products', {
            method: 'POST',
            body: JSON.stringify({ nombre, inventario, categoria_id })
        });
        
        console.log('Producto creado:', nuevoProducto);
        return nuevoProducto;
    } catch (error) {
        console.error('Error creando producto:', error);
        throw error;
    }
}

// Actualizar producto
async function actualizarProducto(id, nombre, inventario, categoria_id) {
    try {
        const productoActualizado = await apiRequest(`/products/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ nombre, inventario, categoria_id })
        });
        
        console.log('Producto actualizado:', productoActualizado);
        return productoActualizado;
    } catch (error) {
        console.error('Error actualizando producto:', error);
        throw error;
    }
}

// Eliminar producto
async function eliminarProducto(id) {
    try {
        const response = await apiRequest(`/products/${id}`, {
            method: 'DELETE'
        });
        
        console.log('Producto eliminado:', response);
        return response;
    } catch (error) {
        console.error('Error eliminando producto:', error);
        throw error;
    }
}

// === FUNCIONES DE CATEGORÍAS ===

// Obtener todas las categorías
async function obtenerCategorias() {
    try {
        const categorias = await apiRequest('/categories', {
            method: 'GET'
        });
        
        console.log('Categorías obtenidas:', categorias);
        return categorias;
    } catch (error) {
        console.error('Error obteniendo categorías:', error);
        throw error;
    }
}

// Crear categoría
async function crearCategoria(nombreCategoria) {
    try {
        const nuevaCategoria = await apiRequest('/categories', {
            method: 'POST',
            body: JSON.stringify({ nombreCategoria })
        });
        
        console.log('Categoría creada:', nuevaCategoria);
        return nuevaCategoria;
    } catch (error) {
        console.error('Error creando categoría:', error);
        throw error;
    }
}

// === FUNCIÓN DE PRUEBA DE CONEXIÓN ===

// Verificar que la API está funcionando
async function verificarConexionAPI() {
    try {
        const response = await apiRequest('/api/health', {
            method: 'GET'
        });
        
        console.log('✅ Conexión con API exitosa:', response);
        return true;
    } catch (error) {
        console.error('❌ Error conectando con API:', error);
        return false;
    }
}

// === EJEMPLO DE USO ===

// Función de ejemplo para probar todas las funciones
async function ejemploCompleto() {
    try {
        console.log('=== INICIANDO PRUEBA DE API ===');
        
        // 1. Verificar conexión
        await verificarConexionAPI();
        
        // 2. Registrar usuario (opcional)
        // await registrarUsuario('testuser', 'testpass123');
        
        // 3. Iniciar sesión
        // await iniciarSesion('testuser', 'testpass123');
        
        // 4. Obtener categorías
        // const categorias = await obtenerCategorias();
        
        // 5. Obtener productos
        // const productos = await obtenerProductos();
        
        console.log('=== PRUEBA COMPLETADA ===');
        
    } catch (error) {
        console.error('Error en ejemplo completo:', error);
    }
}

// Exportar funciones para usar en otros archivos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        registrarUsuario,
        iniciarSesion,
        cerrarSesion,
        obtenerProductos,
        crearProducto,
        actualizarProducto,
        eliminarProducto,
        obtenerCategorias,
        crearCategoria,
        verificarConexionAPI
    };
}

// Auto-verificar conexión al cargar
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Frontend conectado - verificando API...');
    verificarConexionAPI();
});
import os
from flask_cors import CORS

def configure_cors(app):
    """
    Configura CORS para permitir peticiones desde diferentes dominios.
    
    En desarrollo: permite todos los dominios (*)
    En producción: permite todos los dominios con configuración completa
    """
    is_development = os.getenv('FLASK_ENV') == 'development'
    
    # Configuración CORS universal - funciona en desarrollo y producción
    cors_config = {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "*"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,
        "max_age": 3600
    }
    
    # Aplicar configuración CORS a todas las rutas
    CORS(app, 
         resources={r"/*": cors_config},
         supports_credentials=False,
         send_wildcard=True,
         automatic_options=True,
         vary_header=True
    )
    
    return app

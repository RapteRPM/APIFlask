import os
from flask_cors import CORS

def configure_cors(app):
    """
    Configura CORS para permitir peticiones desde diferentes dominios.
    
    En desarrollo: permite todos los dominios (*)
    En producción: permite dominios específicos pero de forma flexible
    """
    is_development = os.getenv('FLASK_ENV') == 'development'
    
    if is_development:
        # Permitir peticiones desde cualquier dominio en desarrollo
        cors_config = {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["*"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False,
            "max_age": 3600
        }
    else:
        # En producción: permitir múltiples dominios conocidos + localhost
        cors_config = {
            "origins": [
                "*",  # Permite todos los dominios en producción
                "http://localhost:3000",
                "http://localhost:5000",
                "http://localhost:8080",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5000",
                "http://127.0.0.1:8080",
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    
    # Aplicar configuración CORS a todas las rutas
    CORS(app, 
         resources={r"/*": cors_config},
         supports_credentials=not is_development
    )
    
    return app

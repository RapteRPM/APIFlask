import os
import logging

def configure_logging():
    """
    Configura el sistema de logging para la aplicación.
    En producción, solo muestra WARNING y ERROR.
    En desarrollo, muestra INFO y DEBUG.
    """
    is_production = os.getenv('FLASK_ENV') == 'production'
    log_level = logging.WARNING if is_production else logging.INFO
    
    # Configurar logger raíz
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Silenciar loggers verbosos
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.INFO if is_production else logging.DEBUG)
    logging.getLogger('flask_cors').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

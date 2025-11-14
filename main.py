from flask import Flask, jsonify
from config.jwt import *
from controller.product_controller import product_bp
from controller.controller_user import user_bp, register_jwt_error_handlers
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.db import Base, engine
from models.models_user import User
from models.product_models import Product, Category

Base.metadata.create_all(bind=engine)
app = Flask(__name__)
    
"""configuracion de jwt"""
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_HEADER_NAME'] = JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = JWT_HEADER_TYPE

jwt = JWTManager(app)

# Configuración CORS más específica para frontend
CORS(app, resources={
    r"/*": {
        "origins": ["*"],  # Permitir todos los orígenes en desarrollo
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

app.register_blueprint(product_bp)
app.register_blueprint(user_bp)

""" Registrar manejadores personalizados de errores JWT"""
register_jwt_error_handlers(app)


@app.route("/")
def index():
    """Endpoint principal de la API"""
    return jsonify({
        "message": "API de Gestión de Productos",
        "version": "1.0",
        "status": "active",
        "cors_enabled": True,
        "endpoints": {
            "auth": {
                "login": "POST /login",
                "register": "POST /registry"
            },
            "products": {
                "list": "GET /products",
                "create": "POST /products", 
                "get": "GET /products/<id>",
                "update": "PUT /products/<id>",
                "delete": "DELETE /products/<id>"
            },
            "categories": {
                "list": "GET /categories",
                "create": "POST /categories"
            },
            "users": {
                "list": "GET /users",
                "get": "GET /users/<id>",
                "update": "PUT /users/<id>",
                "delete": "DELETE /users/<id>"
            }
        }
    })


@app.route("/api/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return jsonify({
        "status": "healthy",
        "timestamp": "2025-11-14",
        "version": "1.0",
        "cors": "enabled"
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

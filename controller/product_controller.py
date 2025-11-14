from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from config.db import get_db_session
from Service.product_service import ProductService, CategoryService


product_bp = Blueprint('product_bp', __name__)

db_session = get_db_session()
product_service = ProductService(db_session)
category_service = CategoryService(db_session)


@product_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """
    GET /categories
    Recupera y retorna todas las categorías disponibles.
    """
    categorias = category_service.listar_categorias()
    return jsonify([
        {'id': c.idCategory, 'nombreCategoria': c.nombreCategoria}
        for c in categorias
    ]), 200


@product_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """
    POST /categories
    Crea una nueva categoría.
    """
    data = request.get_json()
    nombre = data.get('nombreCategoria')
    if not nombre:
        return jsonify({'error': 'El nombre de la categoría es obligatorio'}), 400
    
    try:
        categoria = category_service.crear_categoria(nombre)
        return jsonify({
            'id': categoria.idCategory,
            'nombreCategoria': categoria.nombreCategoria
        }), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    productos = product_service.listar_productos()
    return jsonify([
        {
            'id': p.idProduct,
            'nombre': p.nombre,
            'inventario': p.inventario,
            'categoria': {
                'id': p.categoria.idCategory,
                'nombreCategoria': p.categoria.nombreCategoria
            } if p.categoria else None
        } for p in productos
    ]), 200


@product_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):

    producto = product_service.obtener_producto(product_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': producto.idProduct,
        'nombre': producto.nombre,
        'inventario': producto.inventario,
        'categoria': {
            'id': producto.categoria.idCategory,
            'nombreCategoria': producto.categoria.nombreCategoria
        } if producto.categoria else None
    }), 200


@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    nombre = data.get('nombre')
    inventario = data.get('inventario', 0)
    categoria_id = data.get('categoria_id')

    if not nombre or not categoria_id:
        return jsonify({'error': 'El nombre y la categoría son obligatorios'}), 400

    producto = product_service.crear_producto(nombre, inventario, categoria_id)
    return jsonify({
        'id': producto.idProduct,
        'nombre': producto.nombre,
        'inventario': producto.inventario,
        'categoria_id': producto.categoria_id
    }), 201


@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """
    PUT /products/<product_id>
    Actualiza la información de un producto existente.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    inventario = data.get('inventario')
    categoria_id = data.get('categoria_id')

    producto = product_service.actualizar_producto(product_id, nombre, inventario, categoria_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    return jsonify({
        'id': producto.idProduct,
        'nombre': producto.nombre,
        'inventario': producto.inventario,
        'categoria_id': producto.categoria_id
    }), 200


@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    DELETE /products/<product_id>
    Elimina un producto específico por su ID.
    """
    eliminado = product_service.eliminar_producto(product_id)
    if not eliminado:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({'message': 'Producto eliminado correctamente'}), 200

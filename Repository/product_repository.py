from models.product_models import Product, Category
from sqlalchemy.orm import Session
from typing import Optional


class ProductRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.idProduct == product_id).first()

    def create_product(self, nombre: str, inventario: int, categoria_id: int):
        new_product = Product(nombre=nombre, inventario=inventario, categoria_id=categoria_id)
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def update_product(self, product_id: int, nombre: str = None, inventario: int = None, categoria_id: int = None):
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        if nombre:
            product.nombre = nombre
        if inventario is not None:
            product.inventario = inventario
        if categoria_id:
            product.categoria_id = categoria_id
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> Optional[Product]:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        self.db.delete(product)
        self.db.commit()
        return product


class CategoryRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_categories(self):
        return self.db.query(Category).all()

    def create_category(self, nombre_categoria: str):
        new_category = Category(nombreCategoria=nombre_categoria)
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Category(Base):
    __tablename__ = 'categories'
    idCategory = Column(Integer, primary_key=True, index=True)
    nombreCategoria = Column(String(255), nullable=False, unique=True)

    products = relationship("Product", back_populates="categoria", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = 'products'
    idProduct = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    inventario = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categories.idCategory'), nullable=False)

    categoria = relationship("Category", back_populates="products")

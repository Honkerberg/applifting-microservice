from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String)
    offers = relationship("Offer", back_populates="product")


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = Column(Integer)
    items_in_stock = Column(Integer)
    products = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    product = relationship("Product", back_populates="offers")

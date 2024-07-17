from pydantic import UUID4
from sqlalchemy.orm import Session

from app import models, schemas


def get_product(db: Session, product_id: UUID4):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0):
    return db.query(models.Product).offset(skip).all()


def create_product(db: Session, product: schemas.ProductCreate) -> schemas.ProductResponse:
    db_product = models.Product(name=product.name, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    product_response = schemas.ProductResponse(id=db_product.id, name=db_product.name,
                                               description=db_product.description)
    return product_response


def update_product(db: Session, product_id: UUID4, product: schemas.ProductSchema):
    db_product = get_product(db, product_id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: UUID4):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def create_offer(db: Session, offer: schemas.OfferSchema):
    db_offer = models.Offer(price=offer.price, items_in_stock=offer.items_in_stock, products=offer.product_id)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def get_offers(db: Session, skip: int = 0):
    return db.query(models.Offer).offset(skip).all()

from pydantic import BaseModel, UUID4
import uuid


class OfferSchema(BaseModel):
    price: int
    items_in_stock: int


class OfferCreate(OfferSchema):
    pass


class Offer(OfferSchema):
    id: UUID4
    product_id: UUID4

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    name: str
    description: str


class ProductCreate(ProductSchema):
    pass


class Product(ProductSchema):
    id: UUID4
    offers: list[Offer] = []

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str

import json
import os
import httpx
import uuid

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas, dependencies, models
from app.auth import get_access_token

load_dotenv()

router = APIRouter(tags=["products"])

API_SERVICE_URL = os.getenv("OFFERS_API_URL")


def register_product(product: schemas.ProductResponse):
    """
    Background task to register products
    """
    headers = dict(Bearer=get_access_token())
    data = {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
    }
    with httpx.Client() as client:
        response = client.post(f"{API_SERVICE_URL}/products/register", headers=headers, json=data)
        response.raise_for_status()
        return response.json()


@router.post("/products", response_model=list[schemas.ProductCreate])
async def create_product(products: list[schemas.ProductCreate], background_tasks: BackgroundTasks,
                         db: Session = Depends(dependencies.get_db)):
    """
    Create a new product or list of products.
    """
    for product in products:
        print(product)
        created_product = crud.create_product(db=db, product=product)
        print(created_product)
        background_tasks.add_task(register_product, created_product)
    return products


@router.get("/products", response_model=list[schemas.Product])
async def read_products(skip: int = 0, db: Session = Depends(dependencies.get_db)):
    """
    Get all products from database.
    :return: List of products.
    """
    products = crud.get_products(db=db, skip=skip)
    return products


@router.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: uuid.UUID, db: Session = Depends(dependencies.get_db)):
    """
    Get specific product from database by id.
    """
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: uuid.UUID, product: schemas.ProductSchema,
                         db: Session = Depends(dependencies.get_db)):
    """
    Update specific product from database.
    """
    return crud.update_product(db=db, product_id=product_id, product=product)


@router.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_products(product_id: uuid.UUID, db: Session = Depends(dependencies.get_db)):
    """
    Delete specific product from database.
    """
    return crud.delete_product(db=db, product_id=product_id)


@router.get("/products/{product_id}/offers", response_model=list[schemas.Offer])
async def read_offers(product_id: uuid.UUID, db: Session = Depends(dependencies.get_db)):
    """
    Get offer of specific product.
    """
    db_product = crud.get_product(db=db, product_id=product_id)
    return db_product

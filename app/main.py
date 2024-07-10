from fastapi import FastAPI
from app.database import init_db
from app.api.v1.endpoints import products

from contextlib import asynccontextmanager
from app.events import fetch_and_create_offers


init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await fetch_and_create_offers()
    yield


app = FastAPI(title="Applifting microservice app", version='0.1.0', lifespan=lifespan)
app.include_router(products.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

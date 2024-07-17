from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import crud, schemas, dependencies, models

load_dotenv()

router = APIRouter(tags=["offers"])


@router.get("/offers-list", response_model=list[schemas.OfferResponse])
def get_offers(db: Session = Depends(dependencies.get_db)):
    """
    List of all offers.
    :param db: Database session.
    :return: List of offers from database.
    """
    db_offers = crud.get_offers(db)
    return db_offers

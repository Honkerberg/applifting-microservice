from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from app import models


def update_local_offers(db: Session, product_id: UUID4, offers):
    for offer_data in offers:
        stmt = insert(models.Offer).values(
            id=offer_data['id'],
            price=offer_data['price'],
            items_in_stock=offer_data['items_in_stock'],
            products=product_id
        ).on_conflict_do_update(
            index_elements=['id'],
            set_={
                'price': offer_data['price'],
                'items_in_stock': offer_data['items_in_stock']
            }
        )
        try:
            db.execute(stmt)
        except IntegrityError as e:
            db.rollback()
            print(
                f"IntegrityError updating/inserting offer {offer_data['id']} for product {product_id}: {str(e)}")
            raise
        except Exception as e:
            print(
                f"Unexpected error updating/inserting offer {offer_data['id']} for product {product_id}: {str(e)}")
            raise

    try:
        db.commit()
    except Exception as e:
        print(
            f"Unexpected error occurred: {str(e)}")
        db.rollback()
        raise

    updated_offers = db.query(models.Offer).filter(models.Offer.products == product_id).all()
    print(f"{len(updated_offers)} offers for product {product_id}")

import os

import httpx
from sqlalchemy.exc import SQLAlchemyError

from app.auth import get_access_token
from app.crud import get_products
from app.database import Session
from app.services import update_local_offers


OFFERS_SERVICE_URL = os.getenv('OFFERS_API_URL')


async def fetch_offers():
    db_session = Session()
    access_token = get_access_token()
    headers = {'Bearer': f'{access_token}'}

    try:
        products = get_products(db_session)
        for product in products:
            try:
                with httpx.Client() as client:
                    response = client.get(f'{OFFERS_SERVICE_URL}/products/{product.id}/offers', headers=headers)
                    if response.status_code == 200:
                        offers = response.json()
                        if offers:
                            update_local_offers(db=db_session, product_id=product.id, offers=offers)
                        else:
                            print(f"No offers found for product {product.id}")
            except httpx.HTTPError as exc:
                print(f"HTTP exception for {exc.request.url} - {exc}")
                db_session.rollback()
    except SQLAlchemyError as e:
        print(f"Database error in update_offers_task: {str(e)}")
    finally:
        db_session.close()

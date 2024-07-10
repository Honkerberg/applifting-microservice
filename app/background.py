import os

import httpx

from app.auth import get_access_token
from app.crud import get_products, create_offer
from app.database import Session

OFFERS_SERVICE_URL = os.getenv('OFFERS_API_URL')


async def fetch_offers():
    db_session = Session()
    products = get_products(db_session)
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}

    for product in products:
        with httpx.Client() as client:
            response = client.get(f'{OFFERS_SERVICE_URL}/products/{product.id}/offers', headers=headers)
            if response.status_code == 200:
                offers = response.json()
                for offer in offers:
                    create_offer(db_session, offer)
    db_session.close()

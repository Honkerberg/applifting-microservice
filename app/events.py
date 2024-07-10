import os

from app.background import fetch_offers
from fastapi_utils.tasks import repeat_every
from dotenv import load_dotenv

load_dotenv()

REFRESH_OFFERS = os.getenv("OFFERS_REFRESH_TIME")


@repeat_every(seconds=int(REFRESH_OFFERS))
async def fetch_and_create_offers():
    await fetch_offers()

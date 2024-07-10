from app.background import fetch_offers
from fastapi_utils.tasks import repeat_every


@repeat_every(seconds=60)
async def fetch_and_create_offers():
    await fetch_offers()

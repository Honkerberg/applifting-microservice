import os
import httpx
import json
from dotenv import load_dotenv
from app.redis_service import rd as redis_client


load_dotenv()

API_SERVICE_URL = os.getenv("OFFERS_API_URL")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")


def get_access_token() -> str:
    cache = redis_client.get('access_token')
    if cache:
        print('cache hit')
        return json.loads(cache)['access_token']
    else:
        print('cache miss')
        with httpx.Client() as client:
            headers = dict(Bearer=REFRESH_TOKEN)
            response = client.post(f"{API_SERVICE_URL}/auth", headers=headers)
            response.raise_for_status()
            redis_client.set('access_token', response.text)
            redis_client.expire('access_token', 300)
        return response.json()['access_token']

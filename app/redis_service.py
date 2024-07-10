import os
import redis
from dotenv import load_dotenv


load_dotenv()

rd = redis.Redis(host=os.getenv("REDIS_HOST", 'localhost'), port=6379, db=0)

---
source: Ihorog/cimeika
archived: 2026-02-04
reason: System consolidation
---

from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis

app = FastAPI()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)


class Item(BaseModel):
    key: str
    value: str


@app.get("/")
def read_root():
    return {"message": "CI GPT is running"}


@app.post("/items")
def create_item(item: Item):
    redis_client.set(item.key, item.value)
    return {"status": "stored"}


@app.get("/items/{key}")
def read_item(key: str):
    value = redis_client.get(key)
    return {"key": key, "value": value}

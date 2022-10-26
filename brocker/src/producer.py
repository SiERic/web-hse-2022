import pickle

import pika as pika
import redis as redis
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

MEME_ID = 0


def get_id() -> int:
    global MEME_ID
    MEME_ID += 1
    return MEME_ID


def send_meme(meme: str, id: int):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="memes", durable=True)
    channel.basic_publish(
        exchange="fanout",
        routing_key="memes",
        body=pickle.dumps((meme, id)),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
    )
    connection.close()


class Meme(BaseModel):
    text: str


@router.post("/meme/push")
async def push_meme(meme: Meme):
    id = get_id()
    db = redis.Redis()
    db.set(id, 0)
    send_meme(meme.text, id)
    return id


@router.get("/meme/rating/{id}")
async def get_meme_rating(id: int):
    if id > MEME_ID:
        return 0
    db = redis.Redis()
    return db.get(id)

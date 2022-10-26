import logging
import pickle
import sys

import pika as pika
import redis as redis
from fastapi import APIRouter
from pydantic import BaseModel
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

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
    channel.exchange_declare(exchange="memes", exchange_type="fanout")
    channel.queue_declare(queue="memes", durable=True)

    logger.info("Open connection")

    channel.basic_publish(
        exchange="memes",
        routing_key="",
        body=pickle.dumps((meme, id)),
    )
    connection.close()
    logger.info("Close connection")


class Meme(BaseModel):
    text: str


@router.post("/meme/push/")
async def push_meme(meme: Meme):
    logger.info('New meme push request, test: "%s"', meme.text)
    id = get_id()
    db = redis.Redis()
    db.set(id, 0)
    send_meme(meme.text, id)
    logger.info("Meme successfully sent, id = %d", id)
    return id


@router.get("/meme/rating/{id}")
async def get_meme_rating(id: int):
    if id > MEME_ID:
        return 0
    db = redis.Redis()
    return int(db.get(id))

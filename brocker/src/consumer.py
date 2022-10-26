import logging
import pickle
import sys

import pika
import redis

from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


def callback(ch, method, properties, body):
    (text, id) = pickle.loads(body)
    logger.debug('Got new meme to rate, text: "%s", id: %d', text, id)
    rate = input(f"Rate this meme (id: {id}): (0/1)\n{text}\n").rstrip()
    while rate not in "01":
        rate = input("Rate should be 1 (like) or 0 (not like)").rstrip()
    logger.debug("Meme successfully rated, rate: %s", rate)
    if rate == '1':
        db = redis.Redis()
        db.incr(id, 1)
        logger.debug("Meme (id=%d) rating increased")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
        ),
    )

    channel = connection.channel()
    # channel.exchange_declare("memes", exchange_type="fanout")
    channel.queue_declare(queue="memes", durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="memes", on_message_callback=callback)

    channel.start_consuming()

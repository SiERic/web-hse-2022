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
    print(f"Rate this meme (0/1, 1 = like)\n(id: {id}): {text}")
    rate = input().rstrip()
    while rate not in "01":
        rate = input("Rate should be 1 (like) or 0 (not like)").rstrip()
    logger.debug("Meme successfully rated, rate: %s", rate)
    if rate == '1':
        db = redis.Redis()
        db.incr(id, 1)
        logger.debug("Meme (id=%d) rating increased")


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
        ),
    )

    channel = connection.channel()

    channel.exchange_declare(exchange="memes", exchange_type="fanout")
    queue = channel.queue_declare(queue="", durable=True)
    queue_name = queue.method.queue
    channel.queue_bind(exchange="memes", queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("CONGRATULATIONS !!! YOU ARE A MEME RATER !!!")

    channel.start_consuming()

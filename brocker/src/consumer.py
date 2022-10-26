import pickle

import pika
import redis


def callback(ch, method, properties, body):
    (meme, id) = pickle.loads(body)
    rate = input(f"Rate this meme (id: {id}): (0/1)\n{meme}\n").rstrip()
    while rate not in "01":
        rate = input("Rate should be 1 (like) or 0 (not like)").rstrip()
    if rate == '1':
        db = redis.Redis()
        db.incr(id, 1)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue="memes", durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="memes", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

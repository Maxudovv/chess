import pika
from django.conf import settings


class Rabbit:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials))
        self._channel = self._conn.channel()

    def send_move(self, game_id, move_uci):
        queue_name = f"game_{game_id}"
        self._channel.queue_declare(queue_name)
        self._channel.basic_publish(exchange='',
                                    routing_key=queue_name,
                                    body=move_uci)


rabbitmq = Rabbit()

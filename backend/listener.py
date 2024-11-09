import json

import pika

# credentials = pika.PlainCredentials('reader_user', password="")

# Параметры подключения
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        'localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('reader_user', 'nopass')
    )
)
channel = connection.channel()

# Объявление очереди (необходимо, чтобы убедиться, что она существует)
game_id = "b700ed6b-89e7-46cd-ae55-c8a31c3839d6"
queue_name = f'game_{game_id}'


# Функция обратного вызова для обработки сообщений
def callback(ch, method, properties, body):
    print(f"Получено сообщение: {body.decode()}")
    print(type(body.decode()))
    print(json.loads(body))
    # Подтверждение обработки сообщения
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Прослушивание очереди
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print(f"[*] Ожидание сообщений в {queue_name}. Для выхода нажмите CTRL+C")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()

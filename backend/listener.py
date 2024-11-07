import pika

credentials = pika.PlainCredentials('chess', 'chess')

# Параметры подключения
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Объявление очереди (необходимо, чтобы убедиться, что она существует)
game_id = "dff739a8-4a9e-4b8e-979b-491dd305069c"
queue_name = f'game_{game_id}'


# Функция обратного вызова для обработки сообщений
def callback(ch, method, properties, body):
    print(f"Получено сообщение: {body.decode()}")
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

from django.core.management.base import BaseCommand
from django.conf import settings
import time
import pika

class Command(BaseCommand):
    try:
        help = "Consume Messages From RabbitMQ"

        def handle(self, *args, **kwargs):
            time.sleep(10)
            
            with pika.BlockingConnection(pika.ConnectionParameters(
                        host=settings.RABBITMQ_HOST,
                        port=settings.RABBITMQ_PORT,
                        credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
                )) as connection:

                channel = connection.channel()

                channel.queue_declare(queue="consumer2")

                def callback(ch, method, properties, body):
                    self.stdout.write(self.style.SUCCESS(
                        f"Recieved Message >> {body}"
                    ))

                channel .basic_consume(
                    queue="consumer2", on_message_callback=callback, auto_ack=True
                )

                self.stdout.write(self.style.SUCCESS(
                    "Waiting for messages. To exit Press CTRL + C"
                ))

                channel.start_consuming()

    except Exception as err:
        print(f"Connection Failed >> {err}")
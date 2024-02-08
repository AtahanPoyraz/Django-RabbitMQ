from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import pika
from pika.exceptions import AMQPConnectionError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import traceback
from django.conf import settings
from .serializers import MessageSerializer


def index(request):
    return render(request, "index.html")

def main(request):
    return render(request, "main.html")

def sendmessage(request):
    message = "BU BIR MESAJDIR"
    
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        ))
        channel = connection.channel()

        queue_name = "Messages"

        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange="", routing_key=queue_name, body=message)

        connection.close()

        return HttpResponse("[✓] Mesaj gönderildi")
    except AMQPConnectionError as e:
        print("RabbitMQ Bağlanti Hatasi:", str(e))
        traceback.print_exc()
        return HttpResponse("Hata: Mesaj gönderilemedi")
    
class SendMessage(APIView):
    def post(self, request):
        message = request.data["message"]
        queue_name = request.data["queue_name"]
        serializer = MessageSerializer(data={"message":message,
                                             "queue_name":queue_name})

        if serializer.is_valid():

            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
                ))
                channel = self.connection.channel()

                #queue_name = "Messages"

                channel.queue_declare(queue=queue_name)

                channel.basic_publish(exchange="", routing_key=queue_name, body=message)

                self.connection.close()
                
                return Response({"STATUS":"[✓]",
                                "Message" : message}, status=status.HTTP_200_OK)
        
            except (Exception, AMQPConnectionError) as e:
                traceback.print_exc()
                return Response({"STATUS":"[X]",
                                "Error": e}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"STATUS":"[X]",
                             "Error":serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
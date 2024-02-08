from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import pika
from pika.exceptions import AMQPConnectionError
import time
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

def index(request):
    return render(request, "index.html")
    
def main(request):
    return render(request, "main.html")

def consume_queue(queue_name):
    try:
        while True:
            with pika.BlockingConnection(pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
            )) as connection:
                channel = connection.channel()
                channel.queue_declare(queue=queue_name)

                method_frame, header_frame, body = channel.basic_get(queue=queue_name)
                if method_frame:
                    message = body.decode('utf-8')
                    response = f"[✓] Received message: {message}"
                    return response
                else:
                    response = "[X] No messages available."
                    return response
    except (Exception, AMQPConnectionError) as err:
        return f"[X] Error while consuming messages. {err}"


class GetMessage(APIView):
    def get(self, request):
        response = consume_queue("consumer1")
        time.sleep(1)
        return Response({"message": response}, status=status.HTTP_200_OK)

def getmessage(request):
    response = consume_queue("consumer1")
    time.sleep(1)
    return HttpResponse(response)
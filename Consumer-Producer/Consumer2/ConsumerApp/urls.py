from django.urls import path
from . import views

urlpatterns = [
    path("rabbitmq/", views.getmessage , name="rabbitmq"),
    path("rabbitmq/", views.GetMessage.as_view(), name="rest")
]
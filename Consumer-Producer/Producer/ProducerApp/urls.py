from django.urls import path
from . import views
urlpatterns = [
    path("rabbitmq/", views.sendmessage, name="Producer"),
    path("rabbitmqrest", views.SendMessage.as_view(), name="RestFramework_"),

]
#http://localhost:8001/ninja/docs#/
#http://localhost:8001/api/docs/#/
#http://127.0.0.1:8001/producer/rabbitmq/
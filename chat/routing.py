from django.urls import path
from .consumers import *


websocket_urlpatterns =[
    path('ws/sc/',MyConsumer.as_asgi()),
    path('ws/ac/',MyUpdatedConsumerAC.as_asgi()),
    path('ws/ac-chat/<str:groupName>/',MyChatConsumerAC.as_asgi()),
    path('ws/sc-chat/',MyChatConsumerSC.as_asgi()),
]
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/book/(?P<room_name>\w+)/$',
            consumers.BookConsumer.as_asgi()),
]

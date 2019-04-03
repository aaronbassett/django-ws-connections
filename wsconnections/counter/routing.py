from django.urls import path
from counter.consumers import CountConsumer

websocket_urlpatterns = [
    path('ws/count/<slug:room_name>/', CountConsumer),
]
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
import json
import time

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

class CountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'group_%s' % self.room_name
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

        self.redis_client.incr(f'{self.room_name}:connection_count')
        self.redis_client.set(f'{self.room_name}:last_connection', time.time())

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connection_message',
                'updated': self.redis_client.get(f'{self.room_name}:last_connection').decode("utf-8"),
                'connections': self.redis_client.get(f'{self.room_name}:connection_count').decode("utf-8")
            }
        )

        await self.accept()
    
    async def receive(self, *args, **kwargs):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connection_message',
                'updated': self.redis_client.get(f'{self.room_name}:last_connection').decode("utf-8"),
                'connections': self.redis_client.get(f'{self.room_name}:connection_count').decode("utf-8")
            }
        )

    async def disconnect(self, close_code):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.redis_client.decr(f'{self.room_name}:connection_count')

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connection_message',
                'updated': self.redis_client.get(f'{self.room_name}:last_connection').decode("utf-8"),
                'connections': self.redis_client.get(f'{self.room_name}:connection_count').decode("utf-8")
            }
        )

    # Receive message from room group
    async def connection_message(self, event):
        updated = event['updated']
        connections = event['connections']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'updated': updated,
            'connections': connections
        }))
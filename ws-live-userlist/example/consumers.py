import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class UserConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("user", self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            "user",
            {
                "type": 'is_logged',
                "text": {
                    'username': self.scope["user"].username,
                    'is_logged_in': True
                }
            }
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(
            "user",
            {
                "type": 'is_logged',
                "text": {
                    'username': self.scope["user"].username,
                    'is_logged_in': False
                }
            }
        )
        async_to_sync(self.channel_layer.group_discard)("user", self.channel_name)

    def is_logged(self, event):
        message = event['text']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

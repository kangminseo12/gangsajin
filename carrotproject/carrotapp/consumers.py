# chat_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

		# 클라이언트가 WebSocket 연결을 시도할 때 호출되며,
		# 연결을 수락하고 그룹에 사용자를 추가합니다.
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

		# 클라이언트가 WebSocket 연결을 해제할 때 호출되며,
		# 그룹에서 사용자를 제거합니다.
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

		# 클라이언트로부터 메시지를 받을 때 호출되며,
		# 받은 메시지를 그룹 내의 모든 클라이언트에 전송합니다.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

		# 그룹으로부터 메시지를 받을 때 호출되며,
		# 받은 메시지를 현재 클라이언트에게 전송합니다.	
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from datetime import datetime
from channels.db import database_sync_to_async

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
        
        # 1. '새로운 메시지' 이벤트인 경우
        if text_data_json['type'] == "message_created":
    
            message = text_data_json['message']
            chatroom_id = text_data_json['chatroom_id']
            sender_id = self.scope['user'].id
            receiver_id = text_data_json['receiver_id']
            sent_at = datetime.now().isoformat()
            
            # chatroom_id로 ChatRoom 인스턴스를 가져옵니다.
            chatroom = await self.get_chatroom(chatroom_id)
            
            # 메시지 -> 데이터베이스에 저장
            await self.save_message(chatroom, sender_id, receiver_id, message)

            # room group에 메시지 전달
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'sent_at': sent_at
                }
            )

        # 2. '메시지 읽음' 이벤트인 경우
        if text_data_json['type'] in ["page_clicked", "page_visible", "page_loaded"]:

            chatroom_id = text_data_json['chatroom_id']
            user_id = self.scope['user'].id
            reader_id = text_data_json['reader_id']
            
            # (데이터베이스) 메시지 -> '읽음'으로 업데이트
            await self.update_messages(chatroom_id, user_id)

            # room group에 이벤트 전달
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_message',
                    'reader_id': reader_id
                }
            )

    # 그룹 내의 모든 사용자에게 메시지를 브로드캐스트하기 위해 호출됩니다.
    # 'receive' 함수에서 room group에 메시지를 전송할 때, 아래 chat_message 함수가 메시지를 실제로 브로드캐스트 하는 역할을 한다고 합니다.
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sent_at = event['sent_at']

        await self.send(text_data=json.dumps({
            'type' : 'chat_message',
            'message': message,
            'sender_id': sender_id,
            'sent_at': sent_at
        }))

    # 메시지가 '읽음' 처리되었음을 알리기 위해 호출됩니다.
    async def read_message(self, event):
        reader_id = event['reader_id']
        
        await self.send(text_data=json.dumps({
            'type' : 'read_message',
            'reader_id': reader_id
        }))

    # chatroom의 id로 chatroom 인스턴스를 가져옵니다.
    @database_sync_to_async        
    def get_chatroom(self, chatroom_id):
        return ChatRoom.objects.get(id=chatroom_id)
    
    # 메시지 형식에 맞춰 데이터베이스에 저장합니다
    @database_sync_to_async
    def save_message(self, chatroom_id, sender_id, receiver_id, message):
        Message.objects.create(chatroom=chatroom_id, sender=sender_id, receiver=receiver_id, content=message)

    # 수신자가 현재 로그인한 사용자인 메시지를 모두 '읽음'으로 처리합니다.
    @database_sync_to_async
    def update_messages(self, chatroom_id, user_id):
        messages = Message.objects.filter(chatroom=chatroom_id, receiver=user_id)
        messages.update(is_read=True)

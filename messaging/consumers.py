import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, Conversation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'chat_message')
        
        if message_type == 'chat_message':
            message_content = data['message']
            recipient_id = data['recipient_id']
            message_id = data.get('message_id')
            
            # Save message to database
            message = await self.save_message(message_content, recipient_id)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender': self.user.username,
                    'sender_id': self.user.id,
                    'timestamp': message.created_at.isoformat(),
                    'message_id': message_id or message.id,
                }
            )
        elif message_type == 'message_delivered':
            # Handle delivery confirmation
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_delivered',
                    'message_id': data['message_id'],
                    'recipient': self.user.username
                }
            )
        elif message_type == 'typing':
            # Handle typing indicators
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user': self.user.username,
                    'is_typing': data.get('is_typing', False),
                }
            )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))
    
    async def typing_indicator(self, event):
        # Don't send typing indicator back to sender
        if event['user'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user': event['user'],
                'is_typing': event['is_typing'],
            }))
    
    async def message_delivered(self, event):
        # Send delivery confirmation
        if event['recipient'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'message_delivered',
                'message_id': event['message_id']
            }))
    
    @database_sync_to_async
    def save_message(self, message_content, recipient_id):
        recipient = User.objects.get(id=recipient_id)
        return Message.objects.create(
            sender=self.user,
            recipient=recipient,
            message=message_content,
            message_type='general'
        )
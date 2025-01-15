import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Get the current number of users in the room
        users_in_room = len(await self.channel_layer.group_channels(self.room_group_name))

        # Notify the current user if they are alone
        if users_in_room == 1:
            await self.send(text_data=json.dumps({
                'notification': 'You are the first person in the room. Wait for someone to join.'
            }))
        else:
            # Notify others that a new user has joined
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_joined',
                    'message': f'A user has joined the chat. {users_in_room} users in the room.'
                }
            )

    async def disconnect(self, close_code):
        # Notify others that a user has left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'message': 'A user has left the chat.'
            }
        )

        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()

        if message:
            # Broadcast message to other users
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message']
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message']
        }))

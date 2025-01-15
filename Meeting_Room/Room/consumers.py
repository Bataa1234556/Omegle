import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

# Global pool to manage unpaired users
unpaired_users = []

class OmegleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to the global pool
        self.room_group_name = None
        unpaired_users.append(self)

        # Accept the connection
        await self.accept()

        # Try to pair the user
        await self.pair_user()

    async def disconnect(self, close_code):
        # Remove the user from the global pool if not paired
        if self in unpaired_users:
            unpaired_users.remove(self)

        # Leave the room group if paired
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Forward the message to the other user in the pair
        if self.room_group_name:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data
                }
            )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=event['message'])

    async def pair_user(self):
        global unpaired_users
        if len(unpaired_users) >= 2:
            # Pair the first two users
            user1 = unpaired_users.pop(0)
            user2 = unpaired_users.pop(0)

            # Create a unique room for the pair
            room_name = f"room_{id(user1)}_{id(user2)}"

            # Add both users to the room
            user1.room_group_name = room_name
            user2.room_group_name = room_name

            await self.channel_layer.group_add(
                room_name,
                user1.channel_name
            )
            await self.channel_layer.group_add(
                room_name,
                user2.channel_name
            )

            # Notify users they are paired
            await user1.send(text_data=json.dumps({"message": "You are now connected to a stranger!"}))
            await user2.send(text_data=json.dumps({"message": "You are now connected to a stranger!"}))

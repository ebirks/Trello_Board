from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.board_id = self.scope['url_route']['kwargs']['board_id']

        # Create a unique "room" name for this specific board
        self.room_group_name = f'board_{self.board_id}'

        # Join the group (so everyone looking at this board is in the same room)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()
        print(f"WebSocket connected to board {self.board_id}!")

    async def disconnect(self, close_code):
        # Leave the group when the user disconnects
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    # when someone creates a new card, to broadcast it to everyone in the room.
    async def board_update(self, event):
        # Send the actual message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'board_update',
            'message': event['message']
        }))
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ReactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "reactions"
        self.room_group_name = "reactions_group"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        review_id = data['review_id']
        like = data['like']
        dislike = data['dislike']

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'reaction_message',
                'review_id': review_id,
                'like': like,
                'dislike': dislike
            }
        )

    async def reaction_message(self, event):
        review_id = event['review_id']
        like = event['like']
        dislike = event['dislike']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'review_id': review_id,
            'like': like,
            'dislike': dislike
        }))

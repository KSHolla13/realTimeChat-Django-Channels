import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import *

class ChatConsumer(AsyncWebsocketConsumer):
	def getUser(self, userId):
		return User.objects.get(id=userId)

	def getOnlineUsers(self):
		onlineUsers = OnlineUsers.objects.all()
		return [onlineUser.user.id for onlineUser in onlineUsers]

	def addOnlineUser(self, user):
		try:
			OnlineUsers.objects.create(user=user)
		except:
			pass

	def deleteOnlineUser(self, user):
		try:
			OnlineUsers.objects.get(user=user).delete()
		except:
			pass

	async def sendOnlineUserList(self):
		onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
		chatMessage = {
			'type': 'chat_message',
			'message': {
				'action': 'onlineUser',
				'userList': onlineUserList
			}
		}
		await self.channel_layer.send('onlineUser', chatMessage)


	async def connect(self):
		self.userId = self.scope['url_route']['kwargs']['userId']
		print(self.scope['user'])
		self.user = await database_sync_to_async(self.getUser)(self.userId)
		chat_room = f'user_chatroom_{self.userId}'
		self.chat_room = chat_room
		await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )		
		await self.channel_layer.group_add('onlineUser', self.channel_name)
		await database_sync_to_async(self.addOnlineUser)(self.user)
		await self.sendOnlineUserList()
		await self.accept()
		print('----------------'+self.channel_name)


	async def disconnect(self, close_code):
		await database_sync_to_async(self.deleteOnlineUser)(self.user)
		await self.sendOnlineUserList()


	async def receive(self, text_data):
		message_data = json.loads(text_data)
		send_to_idd= int(message_data["send_to_id"])
		online_users = await database_sync_to_async(self.getOnlineUsers)()
		print(online_users)
		receipent_room = f'user_chatroom_{send_to_idd}'
		my_room = f'user_chatroom_{self.userId}'
		await self.channel_layer.group_send(
            my_room,
            {
				"send_to_id":message_data["send_to_id"],
                "type": "chat_message",	
                "message": message_data["message"],
                "sender_user_id": self.scope['url_route']['kwargs']['userId']
            },
        )

		await self.channel_layer.group_send(
            receipent_room,
            {
				"send_to_id":message_data["send_to_id"],
                "type": "chat_message",
                "message": message_data["message"],
                "sender_user_id": self.scope['url_route']['kwargs']['userId']
            },
        )		

	async def chat_message(self, event):
		await self.send(text_data=json.dumps(event))







	
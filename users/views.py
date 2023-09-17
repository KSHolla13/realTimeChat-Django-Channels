import math
from rest_framework.response import Response
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from users.models import *
from users.serializers import *


class LoginApiView(TokenObtainPairView):
	permission_classes = [AllowAny]
	serializer_class = LoginSerializer


class SignupApiView(CreateAPIView):
	permission_classes = [AllowAny]
	queryset = User.objects.all()
	serializer_class = SignupSerializer


class onlineUserView(ListAPIView):
	queryset = OnlineUsers.objects.all()
	serializer_class = OnlineUsersserializer
	

class allUserView(ListAPIView):
	queryset = User.objects.all()
	serializer_class = allUsersserializer
	pagination_class = LimitOffsetPagination	


class checkUserForChatView(APIView):
	serializer_class = OnlineUsersserializer
	def get(self, request, pk):
		try:
			users = OnlineUsers.objects.all()
			for user in users:
				if user.user.id == pk:
					serializer = OnlineUsersserializer(
            		user, context={'request': request})
					return Response(serializer.data)
				else:
					return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
		except OnlineUsers.DoesNotExist:
			return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
	

class  suggestedFriendsView(APIView):
	serializer_class = allUsersserializer
	def get(self, request, user_id):
		user = User.objects.get(id=user_id)
		with open('C:/Users/Admin/Desktop/django-chat/realTimeChat/users/users.json', 'r') as json_file:
			friends_dataa = json.load(json_file)
			friends_data = friends_dataa.get('users')		

		def calculate_similarity(user, user2):
			if not user or not user2:
				return 0.0  
			dot_product = 0
			magnitude_user1 = 0
			magnitude_user2 = 0
			for i in user.interests.all():	
				interest = i.name
				score_user1 = i.score
				score_user2 = user2['interests'].get(interest, 0)
				dot_product += score_user1 * score_user2
				magnitude_user1 += score_user1 ** 2
				magnitude_user2 += score_user2 ** 2
			if magnitude_user1 == 0 or magnitude_user2 == 0:
				return 0.0  
			cosine_similarity = dot_product / (math.sqrt(magnitude_user1) * math.sqrt(magnitude_user2))
			return cosine_similarity

		suggested_friends = sorted(friends_data,key=lambda user2: calculate_similarity(user,user2),reverse=True)[:5]
		return JsonResponse(suggested_friends, safe=False)

			
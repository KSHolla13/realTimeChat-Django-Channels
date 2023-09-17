from django.urls import re_path
from users import consumers

websocket_urlpatterns = [
	re_path(
		r'ws/users/(?P<userId>\d+)/$',
		consumers.ChatConsumer.as_asgi()
	),
]

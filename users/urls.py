from django.urls import path
from users.views import *

urlpatterns = [	
	path('login', LoginApiView.as_view(), name='login'),
	path('register', SignupApiView.as_view(), name='signup'),
    path('users', allUserView.as_view(), name='alluserList'),
    path('online-users', onlineUserView.as_view(), name='userList'),
    path('chat/start/<int:pk>', checkUserForChatView.as_view(), name='checkUserForChat'),
    path('suggested-friends/<int:user_id>', suggestedFriendsView.as_view(), name='suggested-friends'), 
]

from django.db import models
from django.contrib.auth.models import AbstractUser

class Interest(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    score = models.PositiveIntegerField(null=True,blank=True)
	
class User(AbstractUser):
    age = models.IntegerField(blank=True)
    interests = models.ManyToManyField(Interest)
    def __str__(self):
	    return self.username

class OnlineUsers(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username



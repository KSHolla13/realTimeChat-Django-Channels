from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import * 

class allUsersserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"		
        model=User
		

class OnlineUsersserializer(serializers.ModelSerializer):
	# user = serializers.StringRelatedField(read_only=True)
	class Meta:
		model = OnlineUsers
		fields =['user']
		depth=1

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('name', 'score')
		

class LoginSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['userId'] = user.id
		return token


class SignupSerializer(serializers.ModelSerializer):
	username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	passwordTwo = serializers.CharField(write_only=True, required=True)
	interests = InterestSerializer(many=True)
	class Meta:
		model = User
		fields = (
			'username', 'password', 'passwordTwo','age','interests',
		)
		extra_kwargs = {
			'username': {'required': True},
			'password': {'required': True},
			'age': {'required': True},
		}
	def validate(self, attrs):
		if attrs['password'] != attrs['passwordTwo']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	@transaction.atomic
	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			age=validated_data['age'],
		)
		for interest_data in validated_data["interests"]:
			interest = Interest.objects.create(name=interest_data["name"], score=interest_data["score"])
			user.interests.add(interest)
		user.set_password(validated_data['password'])
		user.save()
		return user
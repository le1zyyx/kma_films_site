from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Movie, Vote, Favorite

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], style={'input_type': 'password'})
    password_check = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_check', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'max_length': 50},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Користувач з таким email вже існує.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Користувач з таким username вже існує.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError({"password_check": "Паролі не співпадають."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_check')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class MovieSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Movie
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Vote
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Favorite
        fields = '__all__'

from rest_framework import serializers
from .models import User, Car


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'language', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        if validated_data['password']:
            user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'language')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'car_name', 'year_of_issue', 'renter')
        read_only_fields = ('id', 'car_name', 'year_of_issue')


class UserCarsSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'cars')


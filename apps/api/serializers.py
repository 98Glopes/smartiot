import datetime
from abc import ABC

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.api.models import Device, Sensor, Read


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        read_only = ['user', 'mqtt_user', 'mqtt_passwd']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = kwargs['context']['request'].user
        self.fields['name'] = serializers.CharField(
            required=True,
            validators=[
                UniqueValidator(queryset=Device.objects.filter(user=user.id))
            ]
        )

    def create(self, validated_data):
        instance = super(DeviceCreateSerializer, self).create(validated_data)
        instance.save()
        return instance


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'device', 'data_type', 'name']


class SensorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'data_type', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = serializers.CharField(
            required=True,
            validators=[
                UniqueValidator(queryset=Sensor.objects.all().filter(device=kwargs['context']['device']))
            ]
        )


class FilterSerializer(serializers.Serializer):
    now = datetime.datetime.now()
    year_ago = now - datetime.timedelta(days=30)

    first_date = serializers.DateTimeField(default=now)
    last_date = serializers.DateTimeField(default=year_ago)

    def create(self, validated_Data):
        return validated_Data


class ListReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Read
        fields = '__all__'

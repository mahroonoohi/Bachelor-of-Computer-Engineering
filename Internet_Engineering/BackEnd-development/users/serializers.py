from rest_framework import serializers


class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)


class LoginOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

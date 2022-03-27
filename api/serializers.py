from rest_framework import serializers


class SimpleChoiceSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

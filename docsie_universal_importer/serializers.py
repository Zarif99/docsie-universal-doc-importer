from rest_framework import serializers
from swag_auth.models import SwaggerStorage


class RepoMapRequestSerializer(serializers.Serializer):
    storage = serializers.PrimaryKeyRelatedField(queryset=SwaggerStorage.objects.all())

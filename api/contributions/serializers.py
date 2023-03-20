from rest_framework import serializers

from contributions.models import Comment
from core import constants


class CommentSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default=constants.CONTRIBUTION_STATUS_NEW)

    class Meta:
        model = Comment
        fields = ["text", "description", "type", "question", "quiz", "status", "created"]

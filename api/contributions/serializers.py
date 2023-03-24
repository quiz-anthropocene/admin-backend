from rest_framework import serializers

from contributions.models import Comment


COMMENT_READ_FIELDS = ["text", "description", "type", "replies", "created"]
COMMENT_REPLY_READ_FIELDS = COMMENT_READ_FIELDS.copy()
COMMENT_REPLY_READ_FIELDS.remove("replies")
COMMENT_FULL_FIELDS = ["text", "description", "type", "question", "quiz", "status", "publish", "created"]
COMMENT_WRITE_FIELDS = COMMENT_FULL_FIELDS.copy()
COMMENT_WRITE_FIELDS.remove("status")
COMMENT_WRITE_FIELDS.remove("publish")


class CommentReplyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = COMMENT_REPLY_READ_FIELDS


class CommentReadSerializer(serializers.ModelSerializer):
    replies = CommentReplyReadSerializer(read_only=True, many=True, source="replies_published")

    class Meta:
        model = Comment
        fields = COMMENT_READ_FIELDS


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = COMMENT_WRITE_FIELDS


class CommentFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = COMMENT_FULL_FIELDS

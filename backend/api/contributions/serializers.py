from rest_framework import serializers

from contributions.models import Contribution


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["text", "description", "type", "question", "quiz", "created"]

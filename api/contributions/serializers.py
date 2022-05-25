from rest_framework import serializers

from contributions.models import Contribution
from core import constants


class ContributionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default=constants.CONTRIBUTION_STATUS_NEW)

    class Meta:
        model = Contribution
        fields = ["text", "description", "type", "question", "quiz", "status", "created"]

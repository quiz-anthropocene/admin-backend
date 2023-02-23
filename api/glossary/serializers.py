from rest_framework import serializers

from glossary.models import GlossaryItem


class GlossaryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryItem
        fields = [
            # "id",
            "name",
            "name_alternatives",
            "definition_short",
            "description",
            "description_accessible_url",
            "language",
            "created",
            "updated",
        ]

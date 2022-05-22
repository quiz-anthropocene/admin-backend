import django_filters

from contributions.models import Contribution


class ContributionFilter(django_filters.FilterSet):
    class Meta:
        model = Contribution
        fields = ["type", "status"]

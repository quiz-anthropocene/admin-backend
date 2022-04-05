import django_filters

from contributions.models import Contribution


class ContributionFilter(django_filters.FilterSet):
    # type = django_filters.ChoiceFilter(
    #     label="Type", choices=constants.CONTRIBUTION_TYPE_CHOICES
    # )  # empty_label="--- Type ---"

    class Meta:
        model = Contribution
        fields = ["type"]

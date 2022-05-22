import factory

from contributions.models import Contribution
from core import constants


class ContributionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contribution

    text = "Une contribution"
    type = constants.CONTRIBUTION_TYPE_COMMENT_APP
    status = constants.CONTRIBUTION_STATUS_PENDING

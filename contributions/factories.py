import factory

from contributions.models import Comment
from core import constants


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = "Une contribution"
    type = constants.CONTRIBUTION_TYPE_COMMENT_APP
    status = constants.CONTRIBUTION_STATUS_PENDING

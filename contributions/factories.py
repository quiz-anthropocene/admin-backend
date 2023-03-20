import factory

from contributions.models import Comment
from core import constants


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = "Une contribution"
    type = constants.COMMENT_TYPE_COMMENT_APP
    status = constants.COMMENT_STATUS_PENDING

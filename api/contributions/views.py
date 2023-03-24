from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.contributions.serializers import CommentWriteSerializer
from contributions.models import Comment


class ContributionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.published()
    serializer_class = CommentWriteSerializer

    @extend_schema(summary="Nouvelle contribution", tags=[Comment._meta.verbose_name], exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

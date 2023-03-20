from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.contributions.serializers import CommentSerializer
from contributions.models import Comment


class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @extend_schema(summary="Nouvelle contribution", tags=[Comment._meta.verbose_name], exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

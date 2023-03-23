from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.contributions.serializers import CommentSerializer
from contributions.models import Comment


class ContributionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.published()
    serializer_class = CommentSerializer

    @extend_schema(summary="Lister tous les commentaires *publiés*", tags=[Comment._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Nouvelle contribution", tags=[Comment._meta.verbose_name], exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.tags.serializers import TagSerializer
from tags.models import Tag


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer

    @extend_schema(summary="Lister tous les tags", tags=[Tag._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.categories.serializers import CategorySerializer
from categories.models import Category


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(summary="Lister toutes les catégories", tags=[Category._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

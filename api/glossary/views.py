from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.glossary.filters import GlossaryItemFilter
from api.glossary.serializers import GlossaryItemSerializer
from glossary.models import GlossaryItem


class GlossaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GlossaryItem.objects.all()
    serializer_class = GlossaryItemSerializer
    filterset_class = GlossaryItemFilter

    @extend_schema(summary="Glossaire", tags=[GlossaryItem._meta.verbose_name])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

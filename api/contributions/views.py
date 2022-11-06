from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.contributions.serializers import ContributionSerializer
from contributions.models import Contribution


class ContributionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

    @extend_schema(summary="Nouvelle contribution", tags=[Contribution._meta.verbose_name], exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

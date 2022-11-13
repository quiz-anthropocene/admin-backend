from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins, viewsets

from api.quizs.filters import QuizFilter
from api.quizs.serializers import QuizSerializer, QuizWithQuestionSerializer
from quizs.models import Quiz


class QuizViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Quiz.objects.public().published()
    serializer_class = QuizSerializer
    filterset_class = QuizFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["id", "publish_date"]

    @extend_schema(summary="Lister tous les quiz *publiés*", tags=[Quiz._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Détail d'un quiz *publié*", tags=[Quiz._meta.verbose_name_plural])
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = QuizWithQuestionSerializer
        return super().retrieve(request, args, kwargs)

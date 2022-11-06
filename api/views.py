import json

from django.db.models import Count, F
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils import sendinblue
from questions.models import Question


def api_home(request):
    return HttpResponse(
        """
        <p>API du Quiz de l'Anthropocène.</p>
        <p>La documentation se trouve à l'adresse <a href="/api/docs/">/api/docs/</a></p>
        """
    )


@api_view(["GET"])
def author_list(request):
    """
    List all authors (with the number of questions per author)
    """
    question_authors = (
        Question.objects.public()
        .validated()
        .values(name=F("author"))
        .annotate(question_count=Count("author"))
        .order_by("-question_count")
    )

    return Response(list(question_authors))


@api_view(["POST"])
def newsletter(request):
    if request.method == "POST":
        try:
            response = sendinblue.newsletter_registration(request.data["email"])
            if response.status_code == 201:
                success_message = (
                    "Votre inscription a été reçu, merci ! "
                    "Vous allez reçevoir un email pour confirmer votre inscription."
                )
                return Response(success_message, status=status.HTTP_201_CREATED)
            elif response.status_code == 204:
                success_message = "Vous êtes déjà inscrit.e :)"
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                raise Exception(json.loads(response._content))
        except Exception as e:
            print(e)
            error_message = f"Erreur lors de votre inscription à la newsletter. {e}"
            return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

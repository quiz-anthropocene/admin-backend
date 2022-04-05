from django.conf import settings

from core.models import Configuration


configuration = Configuration.get_solo()


def expose_settings(request):
    """
    Put things into the context to make them available in templates.
    https://docs.djangoproject.com/en/2.1/ref/templates/api/#using-requestcontext
    """

    return {
        "CONFIGURATION": configuration,
        "METABASE_DASHBOARD_URL": settings.METABASE_DASHBOARD_URL,
    }

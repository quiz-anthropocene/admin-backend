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
        "DEBUG": settings.DEBUG,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "TECH_EMAIL": settings.SERVER_EMAIL,
        "NOTION_HELP_PUBLIC_URL": settings.NOTION_HELP_PUBLIC_URL,
        "METABASE_GENERAL_DASHBOARD_PUBLIC_URL": settings.METABASE_GENERAL_DASHBOARD_PUBLIC_URL,
        "METABASE_QUIZ_DASHBOARD_PUBLIC_URL": settings.METABASE_QUIZ_DASHBOARD_PUBLIC_URL,
        "DISCORD_INVITATION_LINK": settings.DISCORD_INVITATION_LINK,
    }

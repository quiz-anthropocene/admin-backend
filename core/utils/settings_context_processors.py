from django.conf import settings

from core.models import Configuration
from users import constants as user_constants


configuration = Configuration.get_solo()


def expose_settings(request):
    """
    Put things into the context to make them available in templates.
    https://docs.djangoproject.com/en/2.1/ref/templates/api/#using-requestcontext
    """

    return {
        "CONFIGURATION": configuration,
        "DEBUG": settings.DEBUG,
        # emails
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "TECH_EMAIL": settings.SERVER_EMAIL,
        # URLs
        "NOTION_HELP_PUBLIC_URL": settings.NOTION_HELP_PUBLIC_URL,
        "IMPORT_DATA_FROM_NOTION": settings.IMPORT_DATA_FROM_NOTION,
        "METABASE_GENERAL_DASHBOARD_PUBLIC_URL": settings.METABASE_GENERAL_DASHBOARD_PUBLIC_URL,
        "METABASE_QUIZ_DASHBOARD_PUBLIC_URL": settings.METABASE_QUIZ_DASHBOARD_PUBLIC_URL,
        "DISCORD_INVITATION_LINK": settings.DISCORD_INVITATION_LINK,
        # messages
        "IS_ADMIN_MESSAGE": user_constants.IS_ADMIN_MESSAGE,
        "ADMIN_REQUIRED_MESSAGE": user_constants.ADMIN_REQUIRED_MESSAGE,
        "ADMIN_REQUIRED_EDIT_FIELD_MESSAGE": user_constants.ADMIN_REQUIRED_MESSAGE,
        "ONLY_ADMIN_ALLOWED_MESSAGE": user_constants.ONLY_ADMIN_ALLOWED_MESSAGE,
        "ONLY_PRIVATE_QUESTION_AUTHOR_ALLOWED_MESSAGE": user_constants.ONLY_PRIVATE_QUESTION_AUTHOR_ALLOWED_MESSAGE,
        "ONLY_PRIVATE_QUIZ_AUTHOR_ALLOWED_MESSAGE": user_constants.ONLY_PRIVATE_QUIZ_AUTHOR_ALLOWED_MESSAGE,
        "ONLY_QUESTION_AUTHOR_OR_SUPER_CONTRIBUTOR_ALLOWED_MESSAGE": user_constants.ONLY_QUESTION_AUTHOR_OR_SUPER_CONTRIBUTOR_ALLOWED_MESSAGE,  # noqa
        "ONLY_QUIZ_AUTHOR_OR_SUPER_CONTRIBUTOR_ALLOWED_MESSAGE": user_constants.ONLY_QUIZ_AUTHOR_OR_SUPER_CONTRIBUTOR_ALLOWED_MESSAGE,  # noqa
    }

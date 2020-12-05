from django.conf import settings
from django.core import management
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods


def app_home(request):
    return HttpResponse(
        """
        <p>Welcome to the 'Know Your Planet' Backend.</p>
        <p>The api is available at /api</p>
    """
    )


@require_http_methods(["GET"])
def action_aggregate_stats(request):
    """
    Run the daily_stats aggregation command
    """
    if not request.GET.get("token") == settings.GITHUB_CRON_ACTION_TOKEN:
        return HttpResponseForbidden()

    management.call_command("generate_daily_stats")

    return HttpResponse("success")


@require_http_methods(["GET"])
def action_import_questions_from_notion(request):
    """
    Run the import command
    """
    if not request.GET.get("token") == settings.GITHUB_CRON_ACTION_TOKEN:
        return HttpResponseForbidden()

    scope = 0
    management.call_command("import_questions_from_notion", scope)

    return HttpResponse("success")


@require_http_methods(["GET"])
def action_export_data_to_github(request):
    """
    Run the export command
    """
    if not request.GET.get("token") == settings.GITHUB_CRON_ACTION_TOKEN:
        return HttpResponseForbidden()

    management.call_command("export_data_to_github")

    return HttpResponse("success")

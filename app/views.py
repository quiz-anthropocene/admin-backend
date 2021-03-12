from io import StringIO

from django.conf import settings
from django.core import management
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods


out = StringIO()


def app_home(request):
    return HttpResponse(
        """
        <p>Welcome to the 'Know Your Planet' Backend.</p>
        <p>Available endpoints: /api & /stats</p>
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
    management.call_command(
        "import_questions_from_notion", scope, "--skip-old", stdout=out
    )
    result = out.getvalue()

    return HttpResponse(result)


@require_http_methods(["GET"])
def action_export_data_to_github(request):
    """
    Run the export data command
    """
    if not request.GET.get("token") == settings.GITHUB_CRON_ACTION_TOKEN:
        return HttpResponseForbidden()

    management.call_command("export_data_to_github", stdout=out)
    result = out.getvalue()

    return HttpResponse(result)


@require_http_methods(["GET"])
def action_export_stats_to_github(request):
    """
    Run the export stats command
    """
    if not request.GET.get("token") == settings.GITHUB_CRON_ACTION_TOKEN:
        return HttpResponseForbidden()

    management.call_command("export_stats_to_github", stdout=out)
    result = out.getvalue()

    return HttpResponse(result)


@require_http_methods(["GET"])
def action_export_contributions_to_notion(request):
    """
    Run the export contributions command
    """
    if not request.GET.get("token") == settings.GITHUB_CRON_ACTION_TOKEN:
        return HttpResponseForbidden()

    management.call_command("export_contributions_to_notion", stdout=out)
    result = out.getvalue()

    return HttpResponse(result)

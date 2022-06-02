import csv
from datetime import datetime
from io import StringIO

from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.core import management
from django.http import HttpResponse
from solo.admin import SingletonModelAdmin

from categories.models import Category
from core.models import Configuration
from core.utils import utilities
from questions.models import Question
from quizs.models import Quiz
from stats.models import QuestionAnswerEvent, QuestionFeedbackEvent
from tags.models import Tag


class ExportMixin:
    """
    Add export actions
    https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    """

    def export_as_csv(self, request, queryset):
        """
        TODO: improve ManyToMany management (currently: hack to add tags to Question)
        """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.csv"

        # field_names = [field.name for field in self.model._meta.get_fields()]
        field_names = [field.name for field in self.model._meta.fields]

        writer = csv.writer(response)

        if queryset.model.__name__ == "Question":
            writer.writerow(field_names + ["tags", "quizs"])
        else:
            writer.writerow(field_names)

        for obj in queryset:
            if queryset.model.__name__ == "Question":
                writer.writerow(
                    [getattr(obj, field) for field in field_names] + [obj.tags_list_string, obj.quizs_list_string]
                )
            else:
                writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.json"

        response.write(utilities.serialize_queryset_to_json(queryset))

        return response

    def export_as_yaml(self, request, queryset):
        """
        TODO: escape characters " (\") and - (\\-)
        """
        response = HttpResponse(content_type="text/yaml")
        response["Content-Disposition"] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.yaml"

        response.write(utilities.serialize_queryset_to_yaml(queryset))

        return response

    def export_all_question_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Question.objects.all().order_by("pk"))

    def export_all_questionanswerevent_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, QuestionAnswerEvent.objects.all().order_by("pk"))

    def export_all_questionfeedbackevent_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, QuestionFeedbackEvent.objects.all().order_by("pk"))

    def export_all_quiz_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Quiz.objects.all().order_by("pk"))

    def export_all_category_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Category.objects.all().order_by("pk"))

    def export_all_tag_as_yaml(self, request, queryset):
        return self.export_as_yaml(request, Tag.objects.all().order_by("pk"))

    # def export_all_as_yaml(self, request):
    #     meta = self.model._meta

    #     response = HttpResponse(content_type='text/yaml')
    #     response['Content-Disposition'] = 'attachment; filename={}.yaml'.format(meta)

    #     out = StringIO()
    #     management.call_command('dumpdata', 'api.question', '--format=yaml', '--pretty', stdout=out)  # noqa

    #     response.write(out.getvalue())

    #     return response

    export_as_csv.short_description = "Export Selected (CSV)"
    export_as_json.short_description = "Export Selected (JSON)"
    export_as_yaml.short_description = "Export Selected (YAML)"
    export_all_question_as_yaml.short_description = "Export All (YAML)"
    export_all_questionanswerevent_as_yaml.short_description = "Export All (YAML)"
    export_all_questionfeedbackevent_as_yaml.short_description = "Export All (YAML)"
    export_all_quiz_as_yaml.short_description = "Export All (YAML)"
    export_all_category_as_yaml.short_description = "Export All (YAML)"
    export_all_tag_as_yaml.short_description = "Export All (YAML)"


class ConfigurationAdmin(ExportMixin, SingletonModelAdmin):
    EXCLUDED_FIELDS = ["id"]

    # to keep order
    def get_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields if f.name not in self.EXCLUDED_FIELDS]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields if not f.editable]


class LogEntryAdmin(admin.ModelAdmin):
    """
    https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#logentry-objects
    """

    list_display = (
        "object_repr",
        "content_type",
        "action_flag",
        "user",
        "action_time",
    )
    list_filter = (
        "content_type",
        "user",
    )
    ordering = ("-action_time",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MyAdminSite(admin.AdminSite):
    site_header = "Django Admin | Quiz de l'Anthropocène"
    index_title = "Accueil"
    site_title = site_header
    enable_nav_sidebar = False
    index_template = "admin/index_with_export.html"

    def index(self, request, extra_context=None):
        """
        Corresponding template in core/templates/admin/index_with_export.html
        """
        configuration = Configuration.get_solo()
        export_message = ""

        if request.POST.get("run_export_data_to_github_script", False):
            out = StringIO()
            request.POST.get("run_export_data_to_github_script")
            management.call_command("export_data_to_github", stdout=out)
            if configuration.application_open_source_code_url not in out.getvalue():
                export_message = f"Erreur survenue.<br />{out.getvalue()}"
            else:
                export_message = (
                    "La Pull Request a été créé !<br />"
                    "Elle est visible ici : "
                    f"<a href='{out.getvalue()}' target='_blank'>{out.getvalue()}</a>"  # noqa
                )
            print(export_message)
        if request.POST.get("run_export_stats_to_github_script", False):
            out = StringIO()
            request.POST.get("run_export_stats_to_github_script")
            management.call_command("export_stats_to_github", stdout=out)
            if configuration.application_open_source_code_url not in out.getvalue():
                export_message = f"Erreur survenue.<br />{out.getvalue()}"
            else:
                export_message = (
                    "La Pull Request a été créé !<br />"
                    "Elle est visible ici : "
                    f"<a href='{out.getvalue()}' target='_blank'>{out.getvalue()}</a>"  # noqa
                )
            print(export_message)

        extra_context = extra_context or {
            "configuration": configuration,
            "export_message": export_message,
        }

        # Call the superclass index to render the page
        return super().index(request, extra_context=extra_context)


admin_site = MyAdminSite(name="myadmin")

admin_site.register(Configuration, ConfigurationAdmin)
admin_site.register(admin.models.LogEntry, LogEntryAdmin)

admin_site.register(User)
admin_site.register(Permission)
admin_site.register(Group)

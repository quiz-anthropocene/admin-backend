import csv
import json
from datetime import datetime
# from io import StringIO

from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.db.utils import OperationalError
# from django.core.management import call_command

from api.models import Question, QuestionStat, Contribution


class ExportMixin:
    """
    Add export actions
    https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    """
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.csv"
        
        field_names = [field.name for field in self.model._meta.fields]
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.json"
        
        response.write(serializers.serialize("json", queryset, ensure_ascii=False))
        
        return response

    def export_as_yaml(self, request, queryset):
        response = HttpResponse(content_type="text/yaml")
        response['Content-Disposition'] = f"attachment; filename={self.model._meta} - {datetime.now().date()}.yaml"
        
        response.write(serializers.serialize("yaml", queryset).encode().decode("unicode_escape").encode("utf-8"))
        
        return response

    # def export_all_as_yaml(self, request):
    #     meta = self.model._meta

    #     response = HttpResponse(content_type='text/yaml')
    #     response['Content-Disposition'] = 'attachment; filename={}.yaml'.format(meta)

    #     out = StringIO()
    #     call_command('dumpdata', 'api.question', '--format=yaml', '--pretty', stdout=out)

    #     response.write(out.getvalue())

    #     return response

    export_as_csv.short_description = "Export Selected (CSV)"
    export_as_json.short_description = "Export Selected (JSON)"
    export_as_yaml.short_description = "Export Selected (YAML)"
    # export_all_as_yaml.short_description = "Export ALL (YAML)"


class QuestionAdmin(admin.ModelAdmin, ExportMixin):
    list_display = (
        "id", "text", "category", "difficulty", "author", "publish", # "type",
        "has_answer_explanation", "has_answer_additional_links", "has_answer_image_link",
        "answer_count", "answer_success_count",
    )
    list_filter = ("category", "difficulty", "author", "publish",) # "type",
    ordering = ("id",)
    actions = ["export_as_csv", "export_as_json", "export_as_yaml"]


class QuestionStatAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ("id", "question", "answer_choice", "created",)
    ordering = ("id",)
    actions = ["export_as_csv", "export_as_json", "export_as_yaml"]

    def changelist_view(self, request, extra_context=None):
        # Aggregate answers per day
        if settings.DEBUG == True:
            chart_data_query = QuestionStat.objects.extra(select={'day': "date(created)"}) # sqlite
        else:
            chart_data_query = QuestionStat.objects.extra(select={'day': "to_char(created, 'YYYY-MM-DD')"}) # postgresql
        chart_data_query = chart_data_query.values("day").annotate(y=Count("created")).order_by("-day")

        # get answers since today
        if chart_data_query[0]['day'] != str(datetime.now().date()):
            chart_data_list = [{ "day": str(datetime.now().date()), "y": 0 }] + list(chart_data_query)
        else:
            chart_data_list = list(chart_data_query)

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(chart_data_list, cls=DjangoJSONEncoder)
        extra_context = extra_context or { "chart_data": as_json }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionStat, QuestionStatAdmin)
admin.site.register(Contribution)

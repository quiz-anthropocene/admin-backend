import csv
from datetime import datetime
# from io import StringIO

from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers
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


class QuestionStatAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer_choice", "created",)
    ordering = ("id",)

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionStat, QuestionStatAdmin)
admin.site.register(Contribution)

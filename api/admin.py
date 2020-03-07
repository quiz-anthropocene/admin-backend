from django.contrib import admin

from api.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "type", "category", "difficulty",)
    list_filter = ("type", "category", "difficulty",)
    ordering = ("id",)


admin.site.register(Question, QuestionAdmin)

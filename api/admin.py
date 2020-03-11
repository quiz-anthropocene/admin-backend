from django.contrib import admin

from api.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "category", "difficulty", "author", "publish", "has_answer_explanation", "has_answer_additional_links", ) # "type",
    list_filter = ("category", "difficulty", "author", "publish", ) # "type",
    ordering = ("id",)


admin.site.register(Question, QuestionAdmin)

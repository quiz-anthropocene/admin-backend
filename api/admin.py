from django.contrib import admin

from api.models import Question, QuestionStat


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "text", "category", "difficulty", "author", "publish", # "type",
        "has_answer_explanation", "has_answer_additional_links", "has_answer_image_link",
        "answer_count", "answer_success_count",
    )
    list_filter = ("category", "difficulty", "author", "publish",) # "type",
    ordering = ("id",)


class QuestionStatAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer_choice", "created",)
    ordering = ("id",)

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionStat, QuestionStatAdmin)

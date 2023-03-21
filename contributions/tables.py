import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from contributions.models import Comment
from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ChoiceColumn, RichTextLongerEllipsisColumn


COMMENT_FIELDS = ["type", "text", "author", "question", "quiz", "status", "created"]  # id, description


class CommentTable(tables.Table):
    text = RichTextLongerEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    question = tables.Column(
        verbose_name="Question",
        accessor="question.id",
        linkify=lambda record: record.question.get_absolute_url(),
        attrs={"td": {"title": lambda record: record.question}},
    )
    quiz = tables.Column(
        verbose_name="Quiz",
        accessor="quiz.id",
        linkify=lambda record: record.quiz.get_absolute_url(),
        attrs={"td": {"title": lambda record: record.quiz}},
    )
    has_replies_reply = tables.Column(verbose_name=_("Answered"), accessor="has_replies_reply_icon")
    processed_icon = tables.Column(verbose_name=_("Processed"), accessor="processed_icon")
    action = tables.TemplateColumn(
        verbose_name="Actions",
        template_name="contributions/_table_action_items.html",
        attrs={"th": {"style": "min-width:130px"}},
    )

    class Meta:
        model = Comment
        template_name = DEFAULT_TEMPLATE
        fields = COMMENT_FIELDS
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in Comment.COMMENT_CHOICE_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        super().__init__(*args, **kwargs)

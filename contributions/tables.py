import django_tables2 as tables
from django.db.models import Case, Value, When
from django.utils.translation import gettext_lazy as _

from contributions.models import Comment
from core import constants
from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ChoiceColumn, RichTextLongerEllipsisColumn


COMMENT_FIELD_SEQUENCE = [field.name for field in Comment._meta.fields]
COMMENT_FIELD_SEQUENCE.remove("id")
COMMENT_FIELD_SEQUENCE.remove("description")
COMMENT_FIELD_SEQUENCE.remove("parent")
COMMENT_FIELD_SEQUENCE.remove("publish")
COMMENT_FIELD_SEQUENCE.insert(COMMENT_FIELD_SEQUENCE.index("created"), "has_replies_reply")
COMMENT_FIELD_SEQUENCE.insert(COMMENT_FIELD_SEQUENCE.index("created"), "processed")
COMMENT_FIELD_SEQUENCE.insert(COMMENT_FIELD_SEQUENCE.index("created"), "published")


class CommentTable(tables.Table):
    text = RichTextLongerEllipsisColumn(attrs={"td": {"title": lambda record: record.text}})
    question = tables.Column(
        verbose_name=Comment._meta.get_field("question").verbose_name,
        accessor="question.id",
        linkify=lambda record: record.question.get_absolute_url(),
        attrs={"td": {"title": lambda record: record.question}},
    )
    quiz = tables.Column(
        verbose_name=Comment._meta.get_field("quiz").verbose_name,
        accessor="quiz.id",
        linkify=lambda record: record.quiz.get_absolute_url(),
        attrs={"td": {"title": lambda record: record.quiz}},
    )
    has_replies_reply = tables.BooleanColumn(
        yesno="✅,❌",
        verbose_name=_("Answered"),
        accessor="has_replies_reply_icon",
        orderable=False,
    )
    status = tables.Column(
        verbose_name=Comment._meta.get_field("status").verbose_name, order_by=("status_order",), accessor="status"
    )
    processed = tables.Column(
        verbose_name=_("Processed"),
        accessor="processed_icon",
        order_by=("status_order",),
    )
    published = tables.BooleanColumn(
        yesno="✅,❌",
        verbose_name=_("Published"),
        accessor="published_icon",
        orderable=False,
    )
    action = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="contributions/_table_action_items.html",
        attrs={"th": {"style": "min-width:130px"}},
        orderable=False,
    )

    def order_status(self, queryset, is_descending):
        queryset = queryset.annotate(
            status_order=Case(
                When(status=constants.COMMENT_STATUS_NEW, then=Value(1)),
                When(status=constants.COMMENT_STATUS_PENDING, then=Value(2)),
                When(status=constants.COMMENT_STATUS_PROCESSED, then=Value(3)),
                When(status=constants.COMMENT_STATUS_IGNORED, then=Value(4)),
                default=Value(1),
            )
        )
        if is_descending:
            queryset = queryset.order_by("-status_order")
        else:
            queryset = queryset.order_by("status_order")
        return (queryset, True)

    def order_processed(self, queryset, is_descending):
        return self.order_status(queryset, is_descending)

    class Meta:
        model = Comment
        template_name = DEFAULT_TEMPLATE
        fields = COMMENT_FIELD_SEQUENCE
        sequence = COMMENT_FIELD_SEQUENCE
        attrs = DEFAULT_ATTRS

    def __init__(self, *args, **kwargs):
        for field_name in Comment.COMMENT_CHOICE_FIELDS:
            self.base_columns[field_name] = ChoiceColumn()
        super().__init__(*args, **kwargs)

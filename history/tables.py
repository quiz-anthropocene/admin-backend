import django_tables2 as tables

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE


class HistoryTable(tables.Table):
    history_date = tables.DateTimeColumn(verbose_name="Date")
    history_user = tables.Column(verbose_name="Auteur")
    object_model = tables.Column(verbose_name="Type")
    # object_id = tables.Column(verbose_name="ID", accessor="id")
    object_id = tables.TemplateColumn(
        verbose_name="ID",
        template_name="history/_table_id_link.html",
    )
    history_type = tables.Column(verbose_name="Action")
    # history_id = tables.Column()
    history_changed_fields = tables.TemplateColumn(
        verbose_name="Champs modifiés",
        template_name="history/_table_changed_fields_list.html",
        attrs={"td": {"style": "max-width:500px"}},
    )

    class Meta:
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS

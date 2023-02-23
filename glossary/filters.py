import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from glossary.models import GlossaryItem


TEXT_SEARCH_PLACEHOLDER = f"{_('In the following fields:')} " f"{GlossaryItem._meta.get_field('name').verbose_name}"


class GlossaryItemFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        label=_("Text search"),
        method="text_search",
        widget=forms.TextInput(attrs={"placeholder": TEXT_SEARCH_PLACEHOLDER}),
    )

    class Meta:
        model = GlossaryItem
        fields = ["language", "q"]

    def text_search(self, queryset, name, value):
        if not value:
            return queryset
        # normal name filtering
        return queryset.filter(name__icontains=value)

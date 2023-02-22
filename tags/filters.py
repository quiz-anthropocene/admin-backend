import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from tags.models import Tag


TEXT_SEARCH_PLACEHOLDER = f"{_('In the following fields:')} " f"{Tag._meta.get_field('name').verbose_name}"


class TagFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        label=_("Text search"),
        method="name_search",
        widget=forms.TextInput(attrs={"placeholder": TEXT_SEARCH_PLACEHOLDER}),
    )

    class Meta:
        model = Tag
        fields = ["q"]

    def name_search(self, queryset, name, value):
        if not value:
            return queryset
        # normal name filtering
        return queryset.filter(name__icontains=value)

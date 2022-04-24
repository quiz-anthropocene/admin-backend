import django_filters

from tags.models import Tag


class TagFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(label="Nom du tag", method="name_search")

    class Meta:
        model = Tag
        fields = ["q"]

    def name_search(self, queryset, name, value):
        if not value:
            return queryset
        # normal name filtering
        return queryset.filter(name__icontains=value)

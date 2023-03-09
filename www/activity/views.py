from django.views.generic import ListView

from activity.models import Event
from core.mixins import ContributorUserRequiredMixin


class EventListView(ContributorUserRequiredMixin, ListView):
    queryset = Event.objects.display().order_by("-created")
    template_name = "activity/list.html"
    context_object_name = "events"
    paginate_by = 50

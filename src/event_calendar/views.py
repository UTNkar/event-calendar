from django.views.generic import ListView
from event_calendar.models import Event


class EventListView(ListView):
    """The view that lists all events."""

    model = Event
    template_name = "event_list.html"

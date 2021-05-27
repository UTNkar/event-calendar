from django.views.generic import ListView
from event_calendar.models import Event


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"

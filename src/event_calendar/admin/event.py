from django.contrib import admin
from event_calendar.models import EventCoHost


class CoHostInline(admin.TabularInline):  # noqa
    model = EventCoHost
    extra = 1


class EventAdmin(admin.ModelAdmin):  # noqa
    inlines = (CoHostInline,)

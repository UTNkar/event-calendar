from django.contrib import admin
from event_calendar.models import EventCoHost


class CoHostInline(admin.TabularInline):
    model = EventCoHost
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (CoHostInline,)

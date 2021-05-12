from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from .user import UserAdmin
from ..models import (
    User, Event, Group, EventCoHost, Post, Category
)
from .event import EventAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Group, admin.ModelAdmin)
admin.site.register(Post, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(EventCoHost, admin.ModelAdmin)

admin.site.unregister(DjangoGroup)

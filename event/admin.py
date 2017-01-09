from django.contrib import admin
from event.models import Event, Category


class EventAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'short_description', 'created_at']

    class Meta:
        model = Event

admin.site.register(Event, EventAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from .models import Event, Comment, Category, Tag

# Register your models here.
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
from django.contrib import admin

# Register your models here.

from .models import Labels, Organisation, Site, Job

admin.site.register(Labels)
admin.site.register(Organisation)
admin.site.register(Site)
admin.site.register(Job)

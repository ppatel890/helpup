from django.contrib import admin

# Register your models here.
from helpup.models import Project, Donation

admin.site.register(Project)
admin.site.register(Donation)



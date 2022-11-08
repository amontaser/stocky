from django.contrib import admin
from . import models
admin.site.register(models.Organization)
admin.site.register(models.OrganizationLocation)
# Register your models here.

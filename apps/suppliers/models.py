from django.db import models
from django.db import models


#supplier model
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

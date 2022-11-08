import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

#warehouse model is used to define the warehouse of a product
class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Warehouse name", blank=False, null=False, max_length=300)
    location = models.CharField(verbose_name="Warehouse Location",max_length=300,  null=False, blank=False)
    capacity = models.CharField(verbose_name="Capacity",max_length=300,  null=True, blank=True)
    mobile = models.CharField(verbose_name="Mobile",max_length=300,  null=False, blank=False)
    email = models.CharField(verbose_name="Email",max_length=300,  null=False, blank=False)
    active = models.BooleanField(default=True)
    zip = models.CharField(verbose_name="Zip",max_length=300,  null=True, blank=True)
    city = models.CharField(verbose_name="City",max_length=300,  null=True, blank=True)
    state = models.CharField(verbose_name="State",max_length=300,  null=True, blank=True)
    country = models.CharField(verbose_name="Country",max_length=300,  null=True, blank=True)

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
        ordering = ['name']
    
    def __str__(self):
        return self.name

# warehouse racks model is used to define the warehouse racks of a warehouse
class WarehouseRack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    warehouse_id = models.ForeignKey('Warehouse', on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(verbose_name="Rack name", blank=False, null=False, max_length=300)
    location = models.CharField(verbose_name="Rack Location",max_length=300,  null=False, blank=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Warehouse Rack')
        verbose_name_plural = _('Warehouse Racks')
        ordering = ['name']

    def __str__(self):
        return self.name
    
# warehouse shelves model is used to define the warehouse shelves of a warehouse
class WarehouseShelf(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    warehouse_rack_id = models.ForeignKey('WarehouseRack', on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(verbose_name="Shelf name", blank=False, null=False, max_length=300)
    location = models.CharField(verbose_name="Shelf Location",max_length=300,  null=False, blank=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Warehouse Shelf')
        verbose_name_plural = _('Warehouse Shelfs')
        ordering = ['name']
    
    def __str__(self):
        return self.name

from ast import operator
import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


#item unit model
class Unit(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100,unique=True)
    short_name  = models.CharField(max_length=10,unique=True)
    description = models.TextField(blank=True,null=True)
    allow_decimal = models.BooleanField(default=False)
    base_unit_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)


#items model is used to define the items of a product
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(verbose_name="Item code", max_length=300, null=False, blank=False)
    name = models.CharField(verbose_name="Item name", blank=False, null=False, max_length=300)
    description = models.CharField(verbose_name="Item description",max_length=300,  null=False, blank=False)
    type = models.CharField(verbose_name="Item type",max_length=300,  null=False, blank=False)
    unit_id = models.CharField(verbose_name="Unit ID",max_length=300,  null=False, blank=False)
    unit_name = models.CharField(verbose_name="Unit Name",max_length=300,  null=False, blank=False)
    unit_price = models.DecimalField(verbose_name="Unit Price",max_digits=10, decimal_places=2, null=False, blank=False)
    quantity = models.DecimalField(verbose_name="Quantity",max_digits=10, decimal_places=2, null=False, blank=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('items:item_detail', args=[str(self.id)])
    def get_update_url(self):
        return reverse('items:item_update', args=[str(self.id)])
    def get_delete_url(self):
        return reverse('items:item_delete', args=[str(self.id)])
    def get_create_url(self):
        return reverse('items:item_create')
    def get_list_url(self):
        return reverse('items:item_list')
    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        ordering = ['name']

# items warehouse model is used to define the warehouse of a item
class ItemWarehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE, blank=False, null=False)
    warehouse_id = models.ForeignKey('Warehouse', on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.DecimalField(verbose_name="Quantity",max_digits=10, decimal_places=2, null=False, blank=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.item_id.name
    class Meta:
        verbose_name = _('Item Warehouse')
        verbose_name_plural = _('Item Warehouses')
        ordering = ['item_id']

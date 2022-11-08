import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

#variations model is used to define the variations of a product
class Variation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="Variation name", blank=False, null=False, max_length=300)
    description = models.CharField(verbose_name="Variation description",max_length=300,  null=False, blank=False)
    type = models.CharField(verbose_name="Variation type",max_length=300,  null=False, blank=False)
    unit_id = models.CharField(verbose_name="Unit ID",max_length=300,  null=False, blank=False)
    unit_name = models.CharField(verbose_name="Unit Name",max_length=300,  null=False, blank=False)
    unit_price = models.DecimalField(verbose_name="Unit Price",max_digits=10, decimal_places=2, null=False, blank=False)
    quantity = models.DecimalField(verbose_name="Quantity",max_digits=10, decimal_places=2, null=False, blank=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variations')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _('Variation')
        verbose_name_plural = _('Variations')
        ordering = ['name']
        permissions = (
            ("view_variation", "Can view variation"),
        )

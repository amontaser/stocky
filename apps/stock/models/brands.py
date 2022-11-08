import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

#brands model is used to define the brands of a product
class Brand(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(verbose_name="Brand name", blank=False, null=False, max_length=300)
	description = models.CharField(verbose_name="Brand description",max_length=300,  null=False, blank=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('brands:brand_detail', args=[str(self.id)])
	def get_update_url(self):
		return reverse('brands:brand_update', args=[str(self.id)])
	def get_delete_url(self):
		return reverse('brands:brand_delete', args=[str(self.id)])
	def get_create_url(self):
		return reverse('brands:brand_create')
	def get_list_url(self):
		return reverse('brands:brand_list')
	class Meta:
		verbose_name = _('Brand')
		verbose_name_plural = _('Brands')
		ordering = ['name']
		permissions = (
			("view_brand", "Can view brand"),
		)
import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

#category type model is used to define the type of a category
class CategoryType(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(verbose_name="Category type name", blank=False, null=False, max_length=300)
	description = models.CharField(verbose_name="Category type description",max_length=300,  null=False, blank=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('category_types:category_type_detail', args=[str(self.id)])
	def get_update_url(self):
		return reverse('category_types:category_type_update', args=[str(self.id)])
	def get_delete_url(self):
		return reverse('category_types:category_type_delete', args=[str(self.id)])
	def get_create_url(self):
		return reverse('category_types:category_type_create')
	def get_list_url(self):
		return reverse('category_types:category_type_list')
	class Meta:
		verbose_name = _('Category type')
		verbose_name_plural = _('Category types')
		ordering = ['name']
		permissions = (
			("view_category_type", "Can view category type"),
		)
		
	

#category model is used to define the categories of a product
class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(verbose_name="Category name", blank=False, null=False, max_length=300)
	description = models.CharField(verbose_name="Category description",max_length=300,  null=False, blank=False)
	active = models.BooleanField(default=True)
	short_code = models.CharField(verbose_name="Category short code",max_length=300,  null=False, blank=False)


	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('categories:category_detail', args=[str(self.id)])
	def get_update_url(self):
		return reverse('categories:category_update', args=[str(self.id)])
	def get_delete_url(self):
		return reverse('categories:category_delete', args=[str(self.id)])
	def get_create_url(self):
		return reverse('categories:category_create')
	def get_list_url(self):
		return reverse('categories:category_list')
	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')
		ordering = ['name']
		permissions = (
			("view_category", "Can view category"),
		)
import code
from locale import currency
from tkinter import CASCADE
from tkinter.tix import Balloon
from unicodedata import name
from django.forms import CharField, NullBooleanField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model 
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
from apps.common.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from .tax import Tax
import pytz
import avinit

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

User = get_user_model()

#currencychoices is used to define the currency of a tenant
#organization model is used to define the organization of a user
class Organization(models.Model):
	CURRENCY_CHOICES = (
		('USD', 'US Dollar'),
		('EUR', 'Euro'),
		('EGP', 'Egyptian Pound'),	
	)
	
	ORGANIZATION_TYPE_CHOICES = (
		('1', 'Company'),
		('2', 'Individual'),
	)
	SELL_TAX_CHOICES = (
		('1', 'Include'),
		('2', 'Exclude'),
	)
	name = models.CharField(max_length=50, unique=True)
	currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='egp')
	code = models.CharField(max_length=10, unique=True)
	description = models.CharField(max_length=200, blank=True, null=True)
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
	logo = models.ImageField(upload_to='organization/logo/', blank=True, null=True)
	timezone = models.CharField(max_length=50, choices=TIMEZONES, default='UTC')
	type = models.CharField(max_length=50, choices=ORGANIZATION_TYPE_CHOICES, default='company')
	tax_number_1 = models.CharField(max_length=100, blank=True, null=True)
	tax_label_1 = models.CharField(max_length=10, blank=True, null=True)
	tax_number_2 = models.CharField(max_length=100, blank=True, null=True)
	tax_label_2 = models.CharField(max_length=10, blank=True, null=True)
	code_lable_1 = models.CharField(max_length=191, blank=True, null=True)
	code_1 = models.CharField(max_length=191, blank=True, null=True)
	code_lable_2 = models.CharField(max_length=191, blank=True, null=True)
	code_2 = models.CharField(max_length=191, blank=True, null=True)
	defualt_sales_tax = models.ForeignKey(Tax, on_delete=models.CASCADE, blank=True, null=True)
	defualt_profit_precentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	sell_tax = models.CharField(max_length=3, choices=SELL_TAX_CHOICES, default='1')
	logo = models.ImageField(upload_to='organization/logo/', blank=True, null=True)
	sku_prefix = models.CharField(max_length=10, blank=True, null=True)
	exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	

	def __str__(self):
		return self.name
	
	def get_exchange_rate(self):
		if self.exchange_rate:
			return self.exchange_rate
		else:
			return 1
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Organization, self).save(*args, **kwargs)

	def logo_thumbnail(self):
		if self.logo:
			return self.logo.url
		else:
			return None


	def get_absolute_url(self):
		return reverse('organization:organization_detail', kwargs={'slug': self.slug})
	
	def get_edit_url(self):
		return reverse('organization:organization_edit', kwargs={'slug': self.slug})
	
	def get_detail_url(self):
		return reverse('organization:organization_location_detail', kwargs={'pk': self.pk})
	
	def get_delete_url(self):
		return reverse('organization:organization_delete', kwargs={'slug': self.slug})
	
	def get_create_url(self):
		return reverse('organization:organization_location_create')
	
	def get_list_url(self):
		return reverse('organization:organization_list')
	

#organization location model is used to define the location of a organization
class OrganizationLocation(models.Model):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	landmark = models.CharField(max_length=50, blank=True, null=True)
	phone = models.CharField(max_length=50)
	fax = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	website = models.URLField(max_length=200)
	address_line_1 = models.CharField(max_length=100, blank=True)
	address_line_2 = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, blank=True)
	state = models.CharField(max_length=100, blank=True)
	zip_code = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=100, blank=True)
	phone_number = models.CharField(max_length=100, blank=True)
	alternate_phone_number = models.CharField(max_length=100, blank=True)
	fax_number = models.CharField(max_length=100, blank=True)
	latitude = models.CharField(max_length=100, blank=True)
	longitude = models.CharField(max_length=100, blank=True)
	is_primary = models.BooleanField(default=False)
	is_billing = models.BooleanField(default=False)
	is_shipping = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('organization:organization_location_detail', kwargs={'pk': self.pk})
	def get_update_url(self):
		return reverse('organization:organization_location_update', kwargs={'pk': self.pk})
	def get_delete_url(self):
		return reverse('organization:organization_location_delete', kwargs={'pk': self.pk})
	def get_create_url(self):
		return reverse('organization:organization_location_create')
	def get_list_url(self):
		return reverse('organization:organization_location_list')

#organization contact model is used to define the contact of a organization
class OrganizationContact(models.Model):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	is_primary = models.BooleanField(default=False)
	is_billing = models.BooleanField(default=False)
	is_shipping = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('organization:organization_contact_detail', kwargs={'pk': self.pk})
	def get_update_url(self):
		return reverse('organization:organization_contact_update', kwargs={'pk': self.pk})
	def get_delete_url(self):
		return reverse('organization:organization_contact_delete', kwargs={'pk': self.pk})
	def get_create_url(self):
		return reverse('organization:organization_contact_create')
	def get_list_url(self):
		return reverse('organization:organization_contact_list')

#organization tax model is used to define the tax of a organization
class OrganizationTax(models.Model):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	rate = models.DecimalField(max_digits=10, decimal_places=2)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('organization:organization_tax_detail', kwargs={'pk': self.pk})
	def get_update_url(self):
		return reverse('organization:organization_tax_update', kwargs={'pk': self.pk})
	def get_delete_url(self):
		return reverse('organization:organization_tax_delete', kwargs={'pk': self.pk})
	def get_create_url(self):
		return reverse('organization:organization_tax_create')
	def get_list_url(self):
		return reverse('organization:organization_tax_list')


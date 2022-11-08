import code
from locale import currency
import re
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

import pytz


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

#tax rate is used to define the tax rate of a tenant
class Tax(models.Model):
	name = models.CharField(max_length=50, unique=True)
	rate = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.CharField(max_length=200, blank=True, null=True)
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	is_tax_group = models.BooleanField(default=False)
	tax_group = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Tax, self).save(*args, **kwargs)

	def __str__(self):
		return self.name
		
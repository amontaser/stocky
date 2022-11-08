from cProfile import label
from sre_parse import State
from tkinter import Widget
from django import forms
from django.utils.translation import gettext_lazy as _
from apps.accounts.models.user import User
from . import models


class SupplierForm(forms.ModelForm):
	name = forms.CharField(label=_('Tenant Name'), max_length=100 , widget=forms.TextInput(attrs={'class': "form-control"}))
	# domain_url = forms.CharField(label=_('Full Domain Name'), max_length=100 ,required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
	# owner_id = forms.ModelChoiceField(queryset=User.objects.all(),label=_('Tenant Owner'),widget=forms.Select(attrs={'class': "form-select"}))
	# is_active = forms.BooleanField(label=_('Active'),required = False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
	# is_ready = forms.BooleanField(label=_('Ready'),required = False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
	# on_trial = forms.BooleanField(label=_('Trial'),required = False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
	# logo = forms.FileField(label=_('Logo'),required=False,widget=forms.ClearableFileInput(attrs={'class': "form-control"}) )

	class Meta:
		model = models.Supplier
		fields  = ('name',)

	def clean_name(self):
		name = self.cleaned_data['name']
		if name.isnumeric() == True:
			self._errors['name']= self.error_class(["The name must can't be all numeric"])
		if len(name) <= 3:
			self._errors['name']= self.error_class(["The name must be at least %d characters long." % 4])
		return name
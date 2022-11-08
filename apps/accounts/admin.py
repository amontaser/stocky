from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _
from apps.accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
import avinit
User = get_user_model()


class PreConfig(admin.ModelAdmin):
	list_display = ["name","url","action"]

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ['email', 'admin']
	list_filter = ['admin']
	fieldsets = (
		(None, {"fields": ("username", "password")}),
		(_("Personal info"), {"fields": ("first_name","last_name", "email")}),
	   
		(
			_("Permissions"),
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				),
			},
		),
	)
	list_display = ["username", "first_name","last_name", "is_superuser"]

	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2')}
		),
	)
	search_fields = ["first_name","last_name"]
	ordering = ['email']
	filter_horizontal = ()
admin.site.register(User, UserAdmin)


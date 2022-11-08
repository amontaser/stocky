from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse , reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView , ListView, CreateView , DeleteView

from apps.settings.models import organization
from .models import Organization, OrganizationLocation


# @login_required

#organization list view
class OrganizationListView(LoginRequiredMixin, ListView):
    model = organization
    template_name = 'settings/organization/list.html'
    context_object_name = 'organization_list'
    paginate_by = 10
    ordering = ['-id']
    def get_queryset(self):
        return organization.objects.filter(user=self.request.user)

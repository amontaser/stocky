
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms
from django.http import HttpResponseRedirect

# Create your views here.


class SupplierListView(LoginRequiredMixin,generic.ListView):
    model = models.Supplier
    paginate_by = 10
    login_required = True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Suppliers')
        return context

class SupplierCreateView(LoginRequiredMixin,generic.FormView):
    model = models.Supplier
    template_name = 'suppliers/supplier_form.html'
    form_class = forms.SupplierForm
    login_required = True
    fields = '__all__'
        
    def form_valid(self,form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Create Supplier')
        return context

    def get_success_url(self):
        return reverse('suppliers:list')

class SupplierDetailView(LoginRequiredMixin,generic.DetailView):
    model = models.Supplier
    form_class = forms.SupplierForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Supplier Detail')
        return context

class SupplierUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = models.Supplier
    form_class = forms.SupplierForm
    pk_url_kwarg = "pk"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Supplier Update')
        return context

class SupplierDeleteView(generic.DeleteView):
    model = models.Supplier
    success_url = reverse_lazy("suppliers:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Supplier Delete')
        return context
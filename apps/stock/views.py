from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render,reverse,redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import  ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .forms import ItemCreationForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms
from django.http import HttpResponseRedirect

# Create your views here.

@login_required
def index(request):
    context = {'page_title':_('Stock')}
    return render(request, 'stock/index.html', context)

class ItemListView(LoginRequiredMixin,generic.ListView):
    model = models.Item
    template_name = "stock/ItemListView"
    paginate_by = 10
    login_required = True
    queryset = models.Item.objects.all()
    # serializer_class = PollSerializer

    def get_queryset(self):
        tenant = get_tenant(self.request)
        return super().get_queryset().filter(tenant=tenant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Tenants')
        return context


@login_required()
def ItemCreationView(request, uuid):
    # Form processing
    if request.method == 'POST':
        # Create an instance of the form
        form = ItemCreationForm(request.POST)    
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.warehouse = request.user.profile.warehouse
            item.save()
            messages.success(request, f'{item.name} was created successfully')
            # return redirect(reverse('home'))
    form = ItemCreationForm()
            
    context = {
        'form' : form,
    }

    return render(request, 'stock/ItemCreation.html', context)





# List Views
# @cache_page(CACHE_TTL)
def CachedItemListView(request):
    Items = Item.objects.all()
    context = {
        'Items': Items
    }
    return render(request, 'stock/Item_list.html', context)





#Delete Views
class ItemDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = models.Item
    context_object_name = "item"
    pk_url_kwarg = 'id'
    success_url = '/'
    template_name = 'stock/ItemDelete.html'
    success_message = "%(item)s was deleted successfully"



#Update Views
class ItemUpdateView(SuccessMessageMixin, UpdateView):
    model = models.Item
    pk_url_kwarg = 'id'
    template_name_suffix =  '_update_form'
    fields = ['name', 'price', 'sku', 'quantity']
    success_url = '/'
    success_message = "%(name)s was edited successfully"

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse , reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView , ListView, CreateView , DeleteView
from .models import User
# from django.contrib.auth import get_user_model 
# User = get_user_model()

class UserListView(LoginRequiredMixin,ListView):
    model = User
    paginate_by = 10
    login_required = True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Users')
        return context

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = 'id'
    slug_url_kwarg = 'id'

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    slug_field = 'id'
    slug_url_kwarg = 'id'
    fields = ['username', 'email', 'first_name', 'last_name','is_active', 'is_staff', 'is_superuser']
    success_message = _('User updated successfully')
    success_url = reverse_lazy('accounts:user_list')
    login_required = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('User')
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        # form.instance.role = self.request.user.role
        return super().form_valid(form)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse('users:user_detail', kwargs={'username': self.request.user.username})

#create user view
class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    fields = ['username','first_name','last_name','email','role','is_active', 'is_staff', 'is_superuser']
    success_message = _('User successfully created')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Create User')
        return context
    def get_success_url(self):
        return reverse('users:user_list')

#user delete view
class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = _('User successfully deleted')
    success_url = reverse_lazy('users:user_list')
    def get_object(self):
        return self.request.user
    def get_success_url(self):
        return reverse('users:user_list')

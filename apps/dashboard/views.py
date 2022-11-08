from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

@login_required
def index(request):
    user_count =  User.objects.all().count()
    context = {'page_title':_('Dashboard'), 'user_count':user_count}
    return render(request, 'dashboard/index.html', context)
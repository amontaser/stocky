from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
# Create your views here.

def landingView(request):
    context = {'page_title':_('Home')}
    return render(request, 'landing/index.html', context)
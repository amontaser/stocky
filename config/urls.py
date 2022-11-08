from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path , include ,re_path
from django.conf.urls.i18n import i18n_patterns 
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.views.generic import TemplateView

from django_registration.backends.activation.views import RegistrationView

# from apps.accounts.forms import RegisterForm


urlpatterns = [
]

urlpatterns += i18n_patterns(
    # path(r'^i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('apps.landing.urls', namespace='landing')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('settings/', include('apps.settings.urls', namespace='settings')),
    path("stock/", include("apps.stock.urls", namespace="stock")),
    path("users/", include("apps.accounts.urls", namespace="users")),

    # path('accounts/register/',
    #     RegistrationView.as_view(
    #         form_class=RegisterForm,
    #     template_name="account/signup.html",
    #     ),
    #     name='account_signup',
    # ),
    path("accounts/", include("allauth.urls")),
    # path('accounts/', include('django_registration.backends.activation.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        # re_path(r'^media/(?P<path>.*)$', serve, {
        #     'document_root': settings.MEDIA_ROOT,
        # }),
         path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns





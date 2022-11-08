from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('create', views.UserCreateView.as_view(), name='user_create'),
    path("details/<uuid:id>/", views.UserDetailView.as_view(), name="user_detail"),
    path("update/<uuid:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    path("delete/<uuid:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
    path("redirect/", views.UserRedirectView.as_view(), name="user_redirect"),
    
]

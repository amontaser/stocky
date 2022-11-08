from django.urls import path
from . import views

app_name = "stock"
urlpatterns = [
    path('', views.index, name='index'),
    # Products
    path('item', views.ItemListView.as_view(), name="all-item"),
    path('item/all', views.CachedItemListView, name='cached'),
    path('<uuid:uuid>/item/new', views.ItemCreationView, name="add-item"),
    path('item/<int:id>/delete', views.ItemDeleteView.as_view(), name="delete-item"),
    path('item/<int:id>/edit', views.ItemUpdateView.as_view(), name="edit-item"),
]
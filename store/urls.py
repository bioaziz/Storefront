from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.product_list, name='Products'),
    path('products/<int:id>/', views.product_details, name='Products details'),
    path('collections/', views.collection_list, name='Categories'),
    path('collections/<int:id>/', views.collection_details, name='Collections details'),
]
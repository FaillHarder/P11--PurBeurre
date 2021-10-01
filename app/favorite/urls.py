from favorite import views
from django.urls import path

urlpatterns = [
    path('myfood', views.myfood, name='myfood'),
    path('product_save', views.product_save, name='product_save'),
    path('description', views.description, name='description'),
]

from search import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('mentions', views.mentions, name='mentions'),
    path('search_product', views.search_product, name='search_product'),
    path('substitute', views.substitute, name='substitute'),
    path('ajax_search_product', views.ajax_search_product, name='ajax_search_product'),
]

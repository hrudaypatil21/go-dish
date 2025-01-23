from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('get_recipe/', views.get_recipe, name='get_recipe'),
    path('contact/', views.contact, name='contact'),
]

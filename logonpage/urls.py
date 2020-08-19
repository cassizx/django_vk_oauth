from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.index),  
    path('accounts/profile/', views.profile),
    path('accounts/', views.index)
] 
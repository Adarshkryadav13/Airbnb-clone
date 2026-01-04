from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/<int:id>/', views.listing_detail, name='listing_detail'),
]

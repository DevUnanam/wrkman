from django.urls import path
from .views import (
    HomeView, ArtisanListView, artisan_detail_view,
    ContactView, about_view
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('artisans/', ArtisanListView.as_view(), name='artisan_list'),
    path('artisan/<int:pk>/', artisan_detail_view, name='artisan_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', about_view, name='about'),
]
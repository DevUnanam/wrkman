from django.urls import path
from .views import (
    HomeView, ArtisanListView, artisan_detail_view,
    ContactView, about_view, join_as_artisan_view,
    how_it_works_view, success_stories_view, help_center_view
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('artisans/', ArtisanListView.as_view(), name='artisan_list'),
    path('artisan/<int:pk>/', artisan_detail_view, name='artisan_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', about_view, name='about'),
    path('join-as-artisan/', join_as_artisan_view, name='join_as_artisan'),
    path('how-it-works/', how_it_works_view, name='how_it_works'),
    path('success-stories/', success_stories_view, name='success_stories'),
    path('help-center/', help_center_view, name='help_center'),
]
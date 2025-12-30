from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, ClientRegistrationView, ArtisanRegistrationView,
    profile_view, edit_profile_view, get_cities_ajax
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/client/', ClientRegistrationView.as_view(), name='client_register'),
    path('register/artisan/', ArtisanRegistrationView.as_view(), name='artisan_register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('ajax/cities/', get_cities_ajax, name='get_cities'),
]
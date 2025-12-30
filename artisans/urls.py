from django.urls import path
from .views import artisan_profile_view, get_skills_ajax

app_name = 'artisans'

urlpatterns = [
    path('profile/<int:pk>/', artisan_profile_view, name='profile'),
    path('ajax/skills/', get_skills_ajax, name='get_skills'),
]
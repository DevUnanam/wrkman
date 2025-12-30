from django.urls import path
from .views import add_review_view, review_list_view, mark_review_helpful

app_name = 'reviews'

urlpatterns = [
    path('add/<int:artisan_id>/', add_review_view, name='add_review'),
    path('artisan/<int:artisan_id>/', review_list_view, name='review_list'),
    path('helpful/<int:review_id>/', mark_review_helpful, name='mark_helpful'),
]
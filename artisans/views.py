from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ArtisanProfile, Skill


def artisan_profile_view(request, pk):
    """Artisan profile detail view"""
    artisan = get_object_or_404(ArtisanProfile, pk=pk)
    return render(request, 'artisans/profile.html', {'artisan': artisan})


def get_skills_ajax(request):
    """AJAX view to get skills for a category"""
    category_id = request.GET.get('category_id')
    if category_id:
        skills = Skill.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(skills), safe=False)
    return JsonResponse([], safe=False)

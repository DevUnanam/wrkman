from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from artisans.models import ArtisanProfile
from .models import Review, ReviewHelpful
from .forms import ReviewForm


@login_required
def add_review_view(request, artisan_id):
    """Add a review for an artisan"""
    if not request.user.is_client:
        messages.error(request, 'Only clients can leave reviews.')
        return redirect('core:artisan_detail', pk=artisan_id)
    
    artisan = get_object_or_404(ArtisanProfile, pk=artisan_id, is_verified=True)
    
    # Check if user already reviewed this artisan
    if Review.objects.filter(client=request.user, artisan=artisan).exists():
        messages.error(request, 'You have already reviewed this artisan.')
        return redirect('core:artisan_detail', pk=artisan_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = request.user
            review.artisan = artisan
            review.save()
            
            messages.success(request, 'Thank you for your review!')
            return redirect('core:artisan_detail', pk=artisan_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'artisan': artisan,
    }
    return render(request, 'reviews/add_review.html', context)


def review_list_view(request, artisan_id):
    """List all reviews for an artisan"""
    artisan = get_object_or_404(ArtisanProfile, pk=artisan_id, is_verified=True)
    
    reviews = Review.objects.filter(artisan=artisan).select_related(
        'client'
    ).order_by('-created_at')
    
    # Filter by rating if specified
    rating_filter = request.GET.get('rating')
    if rating_filter:
        reviews = reviews.filter(rating=rating_filter)
    
    # Pagination
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    reviews_page = paginator.get_page(page_number)
    
    context = {
        'artisan': artisan,
        'reviews': reviews_page,
        'rating_filter': rating_filter,
        'rating_counts': {
            i: reviews.filter(rating=i).count() for i in range(1, 6)
        },
        'total_reviews': reviews.count(),
    }
    return render(request, 'reviews/review_list.html', context)


@login_required
def mark_review_helpful(request, review_id):
    """Mark a review as helpful or not helpful (AJAX)"""
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)
        is_helpful = request.POST.get('is_helpful') == 'true'
        
        # Remove existing vote if any
        ReviewHelpful.objects.filter(review=review, user=request.user).delete()
        
        # Add new vote
        ReviewHelpful.objects.create(
            review=review,
            user=request.user,
            is_helpful=is_helpful
        )
        
        # Count helpful votes
        helpful_count = ReviewHelpful.objects.filter(
            review=review, 
            is_helpful=True
        ).count()
        
        return JsonResponse({
            'success': True,
            'helpful_count': helpful_count
        })
    
    return JsonResponse({'success': False})

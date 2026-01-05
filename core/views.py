from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.urls import reverse
from artisans.models import ArtisanProfile, Category, State, City
from reviews.models import Review
from .models import FAQ
from .forms import ContactForm, ArtisanSearchForm


class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured categories (top 6 by artisan count)
        featured_categories = Category.objects.annotate(
            artisan_count=Count('artisans')
        ).order_by('-artisan_count')[:6]
        
        # Get top-rated artisans (at least 4.0 rating with 3+ reviews)
        top_artisans = ArtisanProfile.objects.filter(
            is_verified=True,
            user__is_active=True
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).filter(
            avg_rating__gte=4.0,
            review_count__gte=3
        ).order_by('-avg_rating', '-review_count')[:8]
        
        # Recent reviews
        recent_reviews = Review.objects.select_related(
            'client', 'artisan__user'
        ).order_by('-created_at')[:6]
        
        context.update({
            'featured_categories': featured_categories,
            'top_artisans': top_artisans,
            'recent_reviews': recent_reviews,
            'total_artisans': ArtisanProfile.objects.filter(is_verified=True).count(),
            'total_categories': Category.objects.count(),
        })
        
        return context


class ArtisanListView(TemplateView):
    """List and search artisans"""
    template_name = 'core/artisan_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Base queryset
        artisans = ArtisanProfile.objects.filter(
            is_verified=True,
            user__is_active=True
        ).select_related('user', 'category', 'state', 'city').annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        
        # Search and filtering
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')
        state_id = self.request.GET.get('state', '')
        city_id = self.request.GET.get('city', '')
        min_rate = self.request.GET.get('min_rate', '')
        max_rate = self.request.GET.get('max_rate', '')
        min_rating = self.request.GET.get('min_rating', '')
        verified_only = self.request.GET.get('verified_only', '')
        sort_by = self.request.GET.get('sort_by', 'newest')
        
        # Apply filters
        if search_query:
            artisans = artisans.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(skills__name__icontains=search_query) |
                Q(bio__icontains=search_query)
            ).distinct()
        
        if category_id:
            artisans = artisans.filter(category_id=category_id)
        
        if state_id:
            artisans = artisans.filter(state_id=state_id)
        
        if city_id:
            artisans = artisans.filter(city_id=city_id)
        
        if min_rate:
            artisans = artisans.filter(hourly_rate__gte=min_rate)
        
        if max_rate:
            artisans = artisans.filter(hourly_rate__lte=max_rate)
        
        if min_rating:
            artisans = artisans.filter(avg_rating__gte=min_rating)
        
        if verified_only:
            artisans = artisans.filter(is_verified=True)
        
        # Sorting
        if sort_by == 'rating':
            artisans = artisans.order_by('-avg_rating', '-review_count')
        elif sort_by == 'price_low':
            artisans = artisans.order_by('hourly_rate')
        elif sort_by == 'price_high':
            artisans = artisans.order_by('-hourly_rate')
        else:  # newest
            artisans = artisans.order_by('-created_at')
        
        # Pagination
        paginator = Paginator(artisans, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Context data
        context.update({
            'artisans': page_obj,
            'categories': Category.objects.all().order_by('name'),
            'states': State.objects.all().order_by('name'),
            'cities': City.objects.all().order_by('name'),
            'search_query': search_query,
            'category_id': category_id,
            'state_id': state_id,
            'city_id': city_id,
            'min_rate': min_rate,
            'max_rate': max_rate,
            'min_rating': min_rating,
            'verified_only': verified_only,
            'sort_by': sort_by,
            'total_results': paginator.count,
        })
        
        return context


def artisan_detail_view(request, pk):
    """Artisan profile detail view"""
    artisan = get_object_or_404(
        ArtisanProfile.objects.select_related('user', 'category', 'state', 'city'),
        pk=pk,
        is_verified=True,
        user__is_active=True
    )
    
    # Increment profile views
    artisan.increment_views()
    
    # Get reviews with pagination
    reviews = Review.objects.filter(artisan=artisan).select_related(
        'client'
    ).order_by('-created_at')
    
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    reviews_page = paginator.get_page(page_number)
    
    # Check if current user can leave a review
    can_review = (
        request.user.is_authenticated and
        request.user.is_client and
        not Review.objects.filter(client=request.user, artisan=artisan).exists()
    )
    
    # Related artisans (same category, same state)
    related_artisans = ArtisanProfile.objects.filter(
        category=artisan.category,
        state=artisan.state,
        is_verified=True,
        user__is_active=True
    ).exclude(pk=artisan.pk).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:4]
    
    context = {
        'artisan': artisan,
        'reviews': reviews_page,
        'can_review': can_review,
        'related_artisans': related_artisans,
        'skills': artisan.skills.all(),
        'gallery_images': artisan.gallery_images.all()[:6],
    }
    
    return render(request, 'core/artisan_detail.html', context)


class ContactView(FormView):
    """Contact us form view"""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    
    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            'Thank you for your message! We\'ll get back to you soon.'
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context


def about_view(request):
    """About us page"""
    context = {
        'total_artisans': ArtisanProfile.objects.filter(is_verified=True).count(),
        'total_reviews': Review.objects.count(),
        'total_categories': Category.objects.count(),
    }
    return render(request, 'core/about.html', context)


def join_as_artisan_view(request):
    """Join as Artisan page with benefits and call-to-action"""
    context = {
        'total_artisans': ArtisanProfile.objects.filter(is_verified=True).count(),
        'avg_rating': Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0,
        'total_reviews': Review.objects.count(),
    }
    return render(request, 'core/join_as_artisan.html', context)


def how_it_works_view(request):
    """How it Works page explaining platform functionality"""
    context = {
        'total_categories': Category.objects.count(),
        'total_artisans': ArtisanProfile.objects.filter(is_verified=True).count(),
    }
    return render(request, 'core/how_it_works.html', context)


def success_stories_view(request):
    """Success Stories page showcasing reviews and testimonials"""
    # Get top-rated reviews (4 stars and above)
    featured_reviews = Review.objects.filter(
        rating__gte=4
    ).select_related(
        'client', 'artisan__user', 'artisan__category'
    ).order_by('-rating', '-created_at')[:12]
    
    # Get some statistics
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    five_star_reviews = Review.objects.filter(rating=5).count()
    
    context = {
        'featured_reviews': featured_reviews,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'five_star_reviews': five_star_reviews,
        'satisfaction_rate': round((five_star_reviews / total_reviews * 100), 1) if total_reviews > 0 else 0,
    }
    return render(request, 'core/success_stories.html', context)


def help_center_view(request):
    """Redirect Help Center to Contact page"""
    return redirect('core:contact')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import User
from .forms import ClientRegistrationForm, ArtisanRegistrationForm
from artisans.models import ArtisanProfile, Category, State, City


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.is_artisan:
            return reverse_lazy('accounts:artisan_profile')
        return reverse_lazy('core:home')


class ClientRegistrationView(CreateView):
    """Client registration view"""
    model = User
    form_class = ClientRegistrationForm
    template_name = 'accounts/client_register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Registration successful! You can now log in.'
        )
        return response


class ArtisanRegistrationView(CreateView):
    """Artisan registration view"""
    model = User
    form_class = ArtisanRegistrationForm
    template_name = 'accounts/artisan_register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['states'] = State.objects.all()
        return context
    
    def form_valid(self, form):
        user = form.save()
        
        # Create artisan profile
        category_id = self.request.POST.get('category')
        state_id = self.request.POST.get('state')
        city_id = self.request.POST.get('city')
        bio = self.request.POST.get('bio', '')
        hourly_rate = self.request.POST.get('hourly_rate', 0)
        years_experience = self.request.POST.get('years_experience', 0)
        
        if category_id and state_id and city_id:
            category = get_object_or_404(Category, id=category_id)
            state = get_object_or_404(State, id=state_id)
            city = get_object_or_404(City, id=city_id)
            
            artisan_profile = ArtisanProfile.objects.create(
                user=user,
                category=category,
                state=state,
                city=city,
                bio=bio,
                hourly_rate=hourly_rate or 0,
                years_of_experience=years_experience or 0
            )
            
            # Add selected skills
            skill_ids = self.request.POST.getlist('skills')
            if skill_ids:
                artisan_profile.skills.set(skill_ids)
        
        messages.success(
            self.request,
            'Registration successful! Your account is pending approval. '
            'You will be notified once approved.'
        )
        return redirect('accounts:login')


@login_required
def profile_view(request):
    """User profile view"""
    if request.user.is_artisan:
        try:
            artisan_profile = request.user.artisan_profile
            return render(request, 'accounts/artisan_profile.html', {
                'artisan': artisan_profile
            })
        except ArtisanProfile.DoesNotExist:
            messages.error(request, 'Artisan profile not found.')
            return redirect('core:home')
    else:
        return render(request, 'accounts/client_profile.html', {
            'user': request.user
        })


@login_required
def edit_profile_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        # Update basic user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone_number = request.POST.get('phone_number', '')
        
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
        
        request.user.save()
        
        # Update artisan profile if applicable
        if request.user.is_artisan:
            try:
                artisan = request.user.artisan_profile
                artisan.bio = request.POST.get('bio', artisan.bio)
                artisan.hourly_rate = request.POST.get('hourly_rate', artisan.hourly_rate)
                artisan.years_of_experience = request.POST.get('years_experience', artisan.years_of_experience)
                artisan.availability = request.POST.get('availability', artisan.availability)
                
                # Update location if provided
                state_id = request.POST.get('state')
                city_id = request.POST.get('city')
                if state_id and city_id:
                    artisan.state = get_object_or_404(State, id=state_id)
                    artisan.city = get_object_or_404(City, id=city_id)
                
                artisan.save()
                
                # Update skills
                skill_ids = request.POST.getlist('skills')
                if skill_ids:
                    artisan.skills.set(skill_ids)
                    
            except ArtisanProfile.DoesNotExist:
                pass
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    context = {}
    if request.user.is_artisan:
        try:
            context['artisan'] = request.user.artisan_profile
            context['categories'] = Category.objects.all()
            context['states'] = State.objects.all()
            context['cities'] = City.objects.all()
        except ArtisanProfile.DoesNotExist:
            pass
    
    return render(request, 'accounts/edit_profile.html', context)


def get_cities_ajax(request):
    """AJAX view to get cities for a state"""
    state_id = request.GET.get('state_id')
    if state_id:
        cities = City.objects.filter(state_id=state_id).values('id', 'name')
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([], safe=False)

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Categories for artisan services"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Skills that artisans can have"""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class State(models.Model):
    """Nigerian states for location"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=3, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class City(models.Model):
    """Cities within states"""
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['state', 'name']
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"


class ArtisanProfile(models.Model):
    """Extended profile for artisan users"""
    
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artisan_profile')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='artisans')
    skills = models.ManyToManyField(Skill, related_name='artisans')
    bio = models.TextField(
        max_length=1000,
        help_text="Tell potential clients about yourself and your experience"
    )
    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Your hourly rate in Naira"
    )
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField(blank=True, help_text="Optional detailed address")
    availability = models.CharField(
        max_length=12,
        choices=AVAILABILITY_CHOICES,
        default='available'
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the artisan is verified by admin"
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(50)]
    )
    profile_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.category.name}"
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            return round(total_rating / len(reviews), 1)
        return 0.0
    
    @property
    def total_reviews(self):
        """Get total number of reviews"""
        return self.reviews.count()
    
    @property
    def is_top_rated(self):
        """Check if artisan is top rated (4.5+ stars with 5+ reviews)"""
        return self.average_rating >= 4.5 and self.total_reviews >= 5
    
    def increment_views(self):
        """Increment profile views"""
        self.profile_views += 1
        self.save(update_fields=['profile_views'])


class ArtisanGallery(models.Model):
    """Gallery images for artisan work samples"""
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='artisan_gallery/')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Artisan Galleries"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.artisan.user.get_full_name()} - {self.title or 'Gallery Image'}"

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from artisans.models import ArtisanProfile

User = get_user_model()


class Review(models.Model):
    """Reviews and ratings for artisans"""
    
    client = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='given_reviews',
        limit_choices_to={'role': 'client'}
    )
    artisan = models.ForeignKey(
        ArtisanProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(
        max_length=1000,
        help_text="Share your experience with this artisan"
    )
    would_recommend = models.BooleanField(
        default=True,
        help_text="Would you recommend this artisan to others?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['client', 'artisan']  # One review per client per artisan
    
    def __str__(self):
        return f"{self.client.get_full_name()} → {self.artisan.user.get_full_name()} ({self.rating}★)"
    
    @property
    def star_range(self):
        """Return range for template star rendering"""
        return range(1, 6)
    
    @property
    def filled_stars(self):
        """Return range for filled stars"""
        return range(1, self.rating + 1)
    
    @property
    def empty_stars(self):
        """Return range for empty stars"""
        return range(self.rating + 1, 6)


class ReviewHelpful(models.Model):
    """Track if users find reviews helpful"""
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_helpful = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']
    
    def __str__(self):
        helpful_text = "helpful" if self.is_helpful else "not helpful"
        return f"{self.user.username} found review {helpful_text}"


class ReviewReport(models.Model):
    """Report inappropriate reviews"""
    
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Language'),
        ('fake', 'Fake Review'),
        ('personal', 'Personal Attack'),
        ('other', 'Other'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    details = models.TextField(blank=True, max_length=500)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_reports'
    )
    
    class Meta:
        unique_together = ['review', 'reporter']
    
    def __str__(self):
        return f"Report: {self.review} - {self.get_reason_display()}"
    
    def resolve_report(self, admin_user):
        """Mark report as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = admin_user
        self.save()

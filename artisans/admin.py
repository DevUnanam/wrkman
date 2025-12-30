from django.contrib import admin
from .models import Category, Skill, State, City, ArtisanProfile, ArtisanGallery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ('name', 'state__name')


class ArtisanGalleryInline(admin.TabularInline):
    model = ArtisanGallery
    extra = 1


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'category', 'state', 'city', 'hourly_rate', 
        'availability', 'is_verified', 'average_rating', 'total_reviews'
    )
    list_filter = (
        'category', 'state', 'availability', 'is_verified', 
        'years_of_experience', 'created_at'
    )
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'bio'
    )
    filter_horizontal = ('skills',)
    readonly_fields = ('average_rating', 'total_reviews', 'profile_views', 'created_at', 'updated_at')
    inlines = [ArtisanGalleryInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('category', 'skills', 'bio', 'hourly_rate', 'years_of_experience')
        }),
        ('Location', {
            'fields': ('state', 'city', 'address')
        }),
        ('Status', {
            'fields': ('availability', 'is_verified')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_reviews', 'profile_views'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_artisans', 'reject_artisans']
    
    def approve_artisans(self, request, queryset):
        """Approve selected artisans"""
        for artisan in queryset:
            artisan.is_verified = True
            artisan.user.is_active = True
            artisan.user.save()
            artisan.save()
        count = queryset.count()
        self.message_user(request, f'{count} artisan(s) approved successfully.')
    approve_artisans.short_description = "Approve selected artisans"
    
    def reject_artisans(self, request, queryset):
        """Reject selected artisans"""
        for artisan in queryset:
            artisan.is_verified = False
            artisan.user.is_active = False
            artisan.user.save()
            artisan.save()
        count = queryset.count()
        self.message_user(request, f'{count} artisan(s) rejected.')
    reject_artisans.short_description = "Reject selected artisans"


@admin.register(ArtisanGallery)
class ArtisanGalleryAdmin(admin.ModelAdmin):
    list_display = ('artisan', 'title', 'created_at')
    list_filter = ('created_at', 'artisan__category')
    search_fields = ('title', 'artisan__user__username')

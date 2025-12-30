from django.contrib import admin
from django.utils import timezone
from .models import Review, ReviewHelpful, ReviewReport


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'artisan', 'rating', 'title', 'would_recommend',
        'created_at'
    )
    list_filter = (
        'rating', 'would_recommend', 'created_at',
        'artisan__category', 'artisan__state'
    )
    search_fields = (
        'client__username', 'artisan__user__username',
        'title', 'comment'
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Information', {
            'fields': ('client', 'artisan', 'rating', 'title', 'comment', 'would_recommend')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'is_helpful', 'created_at')
    list_filter = ('is_helpful', 'created_at')
    search_fields = ('review__title', 'user__username')


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = (
        'review', 'reporter', 'reason', 'is_resolved',
        'created_at', 'resolved_by'
    )
    list_filter = ('reason', 'is_resolved', 'created_at')
    search_fields = (
        'review__title', 'reporter__username',
        'details', 'resolved_by__username'
    )
    readonly_fields = ('created_at', 'resolved_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('review', 'reporter', 'reason', 'details')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_at', 'resolved_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['resolve_reports']
    
    def resolve_reports(self, request, queryset):
        """Resolve selected reports"""
        count = 0
        for report in queryset.filter(is_resolved=False):
            report.resolve_report(request.user)
            count += 1
        
        self.message_user(request, f'{count} report(s) resolved successfully.')
    resolve_reports.short_description = "Resolve selected reports"

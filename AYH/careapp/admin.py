from django.contrib import admin
from .models import DonorProfile, BloodRequest, Notification, DonorResponse


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'phone', 'is_available', 'created_at')
    list_filter = ('blood_group', 'is_available')
    search_fields = ('user__username', 'user__email', 'phone')
    list_editable = ('is_available',)


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'blood_group', 'units_needed', 'urgency', 'is_active', 'created_by', 'created_at')
    list_filter = ('blood_group', 'urgency', 'is_active', 'created_at')
    search_fields = ('note',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_request', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username',)
    list_editable = ('is_read',)


@admin.register(DonorResponse)
class DonorResponseAdmin(admin.ModelAdmin):
    list_display = ('donor', 'blood_request', 'response', 'responded_at')
    list_filter = ('response', 'responded_at')
    search_fields = ('donor__username',)
    readonly_fields = ('responded_at',)

from django.db import models
from django.contrib.auth.models import User


class DonorProfile(models.Model):
    """Profile for blood donors with contact info and availability"""
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"
    
    class Meta:
        ordering = ['-created_at']


class BloodRequest(models.Model):
    """Blood donation request created by admin"""
    BLOOD_GROUP_CHOICES = DonorProfile.BLOOD_GROUP_CHOICES
    
    URGENCY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
    ]
    
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_needed = models.PositiveIntegerField(default=1)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.blood_group} - {self.urgency} ({self.created_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    """Notification sent to matching donors when a blood request is created"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username} - Request #{self.blood_request.id}"
    
    class Meta:
        unique_together = ('user', 'blood_request')
        ordering = ['-created_at']


class DonorResponse(models.Model):
    """Donor's response (accept/reject) to a blood request"""
    RESPONSE_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='responses')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_responses')
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES)
    responded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor.username} - {self.response} (Request #{self.blood_request.id})"
    
    class Meta:
        unique_together = ('blood_request', 'donor')
        ordering = ['-responded_at']

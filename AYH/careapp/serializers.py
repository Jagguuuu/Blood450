"""
API Serializers for Blood Donation System
Converts Django models to/from JSON for REST API
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DonorProfile, BloodRequest, Notification, DonorResponse


# ==============================================================================
# USER SERIALIZERS
# ==============================================================================

class UserSerializer(serializers.ModelSerializer):
    """Basic user information"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration with password"""
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        """Validate password match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# ==============================================================================
# DONOR PROFILE SERIALIZERS
# ==============================================================================

class DonorProfileSerializer(serializers.ModelSerializer):
    """Donor profile with user information"""
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DonorProfile
        fields = [
            'id',
            'user',
            'username',
            'phone',
            'blood_group',
            'is_available',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DonorProfileCreateSerializer(serializers.ModelSerializer):
    """Create/Update donor profile"""
    
    class Meta:
        model = DonorProfile
        fields = ['phone', 'blood_group', 'is_available']
    
    def validate_phone(self, value):
        """Validate phone number format"""
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with country code (e.g., +1)")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number is too short")
        return value


class DonorProfileListSerializer(serializers.ModelSerializer):
    """Simplified donor list for admin"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = DonorProfile
        fields = ['id', 'username', 'email', 'phone', 'blood_group', 'is_available', 'created_at']


# ==============================================================================
# BLOOD REQUEST SERIALIZERS
# ==============================================================================

class BloodRequestSerializer(serializers.ModelSerializer):
    """Blood request with creator information"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    notified_count = serializers.SerializerMethodField()
    accepted_count = serializers.SerializerMethodField()
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = [
            'id',
            'blood_group',
            'units_needed',
            'urgency',
            'urgency_display',
            'note',
            'created_by',
            'created_by_username',
            'is_active',
            'created_at',
            'notified_count',
            'accepted_count'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
    
    def get_notified_count(self, obj):
        """Count of notified donors"""
        return obj.notifications.count()
    
    def get_accepted_count(self, obj):
        """Count of donors who accepted"""
        return obj.responses.filter(response='accepted').count()


class BloodRequestCreateSerializer(serializers.ModelSerializer):
    """Create blood request"""
    
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'units_needed', 'urgency', 'note']
    
    def validate_units_needed(self, value):
        """Validate units is positive"""
        if value < 1:
            raise serializers.ValidationError("Units needed must be at least 1")
        if value > 10:
            raise serializers.ValidationError("Units needed cannot exceed 10")
        return value


class BloodRequestDetailSerializer(serializers.ModelSerializer):
    """Detailed blood request with responses"""
    created_by = UserSerializer(read_only=True)
    notified_donors = serializers.SerializerMethodField()
    accepted_donors = serializers.SerializerMethodField()
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = [
            'id',
            'blood_group',
            'units_needed',
            'urgency',
            'urgency_display',
            'note',
            'created_by',
            'is_active',
            'created_at',
            'notified_donors',
            'accepted_donors'
        ]
    
    def get_notified_donors(self, obj):
        """List of notified donors"""
        notifications = obj.notifications.select_related('user__donor_profile').all()
        return [{
            'id': n.user.id,
            'username': n.user.username,
            'blood_group': n.user.donor_profile.blood_group if hasattr(n.user, 'donor_profile') else None,
            'notified_at': n.created_at
        } for n in notifications]
    
    def get_accepted_donors(self, obj):
        """List of donors who accepted"""
        responses = obj.responses.filter(response='accepted').select_related('donor__donor_profile')
        return [{
            'id': r.donor.id,
            'username': r.donor.username,
            'phone': r.donor.donor_profile.phone if hasattr(r.donor, 'donor_profile') else None,
            'blood_group': r.donor.donor_profile.blood_group if hasattr(r.donor, 'donor_profile') else None,
            'responded_at': r.responded_at
        } for r in responses]


# ==============================================================================
# NOTIFICATION SERIALIZERS
# ==============================================================================

class NotificationSerializer(serializers.ModelSerializer):
    """Notification with blood request details"""
    blood_request = BloodRequestSerializer(read_only=True)
    has_responded = serializers.SerializerMethodField()
    response_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'blood_request',
            'is_read',
            'created_at',
            'has_responded',
            'response_status'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_has_responded(self, obj):
        """Check if donor has responded"""
        user = self.context.get('request').user if self.context.get('request') else None
        if user:
            return DonorResponse.objects.filter(
                blood_request=obj.blood_request,
                donor=user
            ).exists()
        return False
    
    def get_response_status(self, obj):
        """Get donor's response status"""
        user = self.context.get('request').user if self.context.get('request') else None
        if user:
            try:
                response = DonorResponse.objects.get(
                    blood_request=obj.blood_request,
                    donor=user
                )
                return response.response
            except DonorResponse.DoesNotExist:
                return None
        return None


# ==============================================================================
# DONOR RESPONSE SERIALIZERS
# ==============================================================================

class DonorResponseSerializer(serializers.ModelSerializer):
    """Donor response to blood request"""
    donor = UserSerializer(read_only=True)
    blood_request = BloodRequestSerializer(read_only=True)
    response_display = serializers.CharField(source='get_response_display', read_only=True)
    
    class Meta:
        model = DonorResponse
        fields = [
            'id',
            'blood_request',
            'donor',
            'response',
            'response_display',
            'responded_at'
        ]
        read_only_fields = ['id', 'donor', 'responded_at']


class DonorResponseCreateSerializer(serializers.ModelSerializer):
    """Create donor response"""
    
    class Meta:
        model = DonorResponse
        fields = ['blood_request', 'response']
    
    def validate_response(self, value):
        """Validate response value"""
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Response must be 'accepted' or 'rejected'")
        return value
    
    def validate(self, data):
        """Check if donor already responded"""
        user = self.context['request'].user
        blood_request = data['blood_request']
        
        if DonorResponse.objects.filter(blood_request=blood_request, donor=user).exists():
            raise serializers.ValidationError("You have already responded to this request")
        
        return data


# ==============================================================================
# DASHBOARD SERIALIZERS
# ==============================================================================

class DashboardStatsSerializer(serializers.Serializer):
    """Admin dashboard statistics"""
    total_requests = serializers.IntegerField()
    active_requests = serializers.IntegerField()
    total_donors = serializers.IntegerField()
    available_donors = serializers.IntegerField()
    total_accepted = serializers.IntegerField()
    critical_requests = serializers.IntegerField()
    recent_requests = BloodRequestSerializer(many=True)

"""
REST API Views for Blood Donation System
Provides JSON endpoints for Flutter mobile app
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404

from .models import DonorProfile, BloodRequest, Notification, DonorResponse
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    DonorProfileSerializer,
    DonorProfileCreateSerializer,
    DonorProfileListSerializer,
    BloodRequestSerializer,
    BloodRequestCreateSerializer,
    BloodRequestDetailSerializer,
    NotificationSerializer,
    DonorResponseSerializer,
    DonorResponseCreateSerializer,
    DashboardStatsSerializer,
)
from .views import get_compatible_blood_groups  # Import blood compatibility logic


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint - Returns JWT tokens
    
    POST /api/auth/login/
    Body: {
        "username": "admin",
        "password": "admin123"
    }
    
    Response: {
        "access": "jwt_access_token",
        "refresh": "jwt_refresh_token",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "is_staff": true
        }
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Check if user has donor profile
        has_profile = hasattr(user, 'donor_profile')
        donor_profile = None
        if has_profile:
            donor_profile = DonorProfileSerializer(user.donor_profile).data
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'has_donor_profile': has_profile,
            'donor_profile': donor_profile
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register new donor
    
    POST /api/auth/register/
    Body: {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepass123",
        "password_confirm": "securepass123",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout - Blacklist refresh token
    
    POST /api/auth/logout/
    Body: {
        "refresh": "jwt_refresh_token"
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Get current authenticated user
    
    GET /api/auth/me/
    """
    user = request.user
    has_profile = hasattr(user, 'donor_profile')
    donor_profile = None
    
    if has_profile:
        donor_profile = DonorProfileSerializer(user.donor_profile).data
    
    return Response({
        'user': UserSerializer(user).data,
        'has_donor_profile': has_profile,
        'donor_profile': donor_profile
    })


# ==============================================================================
# DONOR PROFILE VIEWS
# ==============================================================================

class DonorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for donor profiles
    
    GET    /api/donors/           - List all donors (admin only)
    POST   /api/donors/           - Create donor profile
    GET    /api/donors/{id}/      - Get donor details
    PUT    /api/donors/{id}/      - Update donor profile
    DELETE /api/donors/{id}/      - Delete donor profile
    GET    /api/donors/me/        - Get current user's profile
    """
    queryset = DonorProfile.objects.all().select_related('user')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DonorProfileCreateSerializer
        elif self.action == 'list':
            return DonorProfileListSerializer
        return DonorProfileSerializer
    
    def get_permissions(self):
        """Admin can see all, donors can see their own"""
        if self.action == 'list':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Create profile for current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's donor profile"""
        try:
            profile = DonorProfile.objects.get(user=request.user)
            serializer = DonorProfileSerializer(profile)
            return Response(serializer.data)
        except DonorProfile.DoesNotExist:
            return Response(
                {'error': 'Donor profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Update current user's donor profile"""
        try:
            profile = DonorProfile.objects.get(user=request.user)
            serializer = DonorProfileCreateSerializer(
                profile,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(DonorProfileSerializer(profile).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DonorProfile.DoesNotExist:
            return Response(
                {'error': 'Donor profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ==============================================================================
# BLOOD REQUEST VIEWS
# ==============================================================================

class BloodRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for blood requests
    
    GET    /api/blood-requests/              - List all requests
    POST   /api/blood-requests/              - Create request (admin only)
    GET    /api/blood-requests/{id}/         - Get request details
    PUT    /api/blood-requests/{id}/         - Update request (admin only)
    DELETE /api/blood-requests/{id}/         - Delete request (admin only)
    GET    /api/blood-requests/active/       - Get active requests
    GET    /api/blood-requests/my-requests/  - Get requests created by me (admin)
    """
    queryset = BloodRequest.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BloodRequestCreateSerializer
        elif self.action == 'retrieve':
            return BloodRequestDetailSerializer
        return BloodRequestSerializer
    
    def get_permissions(self):
        """Admin can create/update/delete, all authenticated users can view"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @transaction.atomic
    def perform_create(self, serializer):
        """
        Create blood request and notify compatible donors
        Uses the same blood compatibility logic as web version
        """
        blood_request = serializer.save(created_by=self.request.user)
        
        # Get compatible blood groups
        compatible_blood_groups = get_compatible_blood_groups(blood_request.blood_group)
        
        # Find matching donors
        matching_donors = DonorProfile.objects.filter(
            blood_group__in=compatible_blood_groups,
            is_available=True
        ).select_related('user')
        
        # Create notifications
        notifications_created = 0
        for donor_profile in matching_donors:
            try:
                Notification.objects.create(
                    user=donor_profile.user,
                    blood_request=blood_request
                )
                notifications_created += 1
            except IntegrityError:
                pass
        
        # Add notification count to response
        blood_request.notifications_count = notifications_created
    
    def create(self, request, *args, **kwargs):
        """Override create to return custom response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        blood_request = serializer.instance
        response_serializer = BloodRequestDetailSerializer(blood_request)
        
        return Response({
            'message': f'Blood request created successfully! {getattr(blood_request, "notifications_count", 0)} compatible donor(s) notified.',
            'blood_request': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active blood requests"""
        active_requests = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        """Get blood requests created by current user (admin)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        my_requests = self.queryset.filter(created_by=request.user)
        serializer = self.get_serializer(my_requests, many=True)
        return Response(serializer.data)


# ==============================================================================
# NOTIFICATION VIEWS
# ==============================================================================

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for notifications (read-only for donors)
    
    GET    /api/notifications/           - List my notifications
    GET    /api/notifications/{id}/      - Get notification details
    POST   /api/notifications/{id}/mark-read/ - Mark as read
    POST   /api/notifications/mark-all-read/ - Mark all as read
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only show notifications for current user"""
        return Notification.objects.filter(
            user=self.request.user
        ).select_related('blood_request', 'blood_request__created_by').order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({'message': f'{count} notifications marked as read'})


# ==============================================================================
# DONOR RESPONSE VIEWS
# ==============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_request(request):
    """
    Donor responds to blood request (accept/reject)
    
    POST /api/respond/
    Body: {
        "blood_request_id": 1,
        "response": "accepted"  // or "rejected"
    }
    """
    blood_request_id = request.data.get('blood_request_id')
    response_value = request.data.get('response')
    
    if not blood_request_id or not response_value:
        return Response(
            {'error': 'blood_request_id and response are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if response_value not in ['accepted', 'rejected']:
        return Response(
            {'error': 'response must be "accepted" or "rejected"'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    blood_request = get_object_or_404(BloodRequest, id=blood_request_id)
    
    # Create or update response
    donor_response, created = DonorResponse.objects.update_or_create(
        blood_request=blood_request,
        donor=request.user,
        defaults={'response': response_value}
    )
    
    # Mark notification as read
    Notification.objects.filter(
        user=request.user,
        blood_request=blood_request
    ).update(is_read=True)
    
    action = 'created' if created else 'updated'
    
    return Response({
        'message': f'Response {action} successfully',
        'response': DonorResponseSerializer(donor_response).data
    }, status=status.HTTP_200_OK)


# ==============================================================================
# DASHBOARD VIEWS
# ==============================================================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    """
    Admin dashboard statistics
    
    GET /api/dashboard/
    """
    total_requests = BloodRequest.objects.count()
    active_requests = BloodRequest.objects.filter(is_active=True).count()
    total_donors = DonorProfile.objects.count()
    available_donors = DonorProfile.objects.filter(is_available=True).count()
    total_accepted = DonorResponse.objects.filter(response='accepted').count()
    critical_requests = BloodRequest.objects.filter(urgency='critical', is_active=True).count()
    
    # Recent requests
    recent_requests = BloodRequest.objects.all().order_by('-created_at')[:10]
    
    data = {
        'total_requests': total_requests,
        'active_requests': active_requests,
        'total_donors': total_donors,
        'available_donors': available_donors,
        'total_accepted': total_accepted,
        'critical_requests': critical_requests,
        'recent_requests': BloodRequestSerializer(recent_requests, many=True).data
    }
    
    return Response(data)

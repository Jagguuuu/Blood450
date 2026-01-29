from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import IntegrityError, transaction
import json

from .models import BloodRequest, DonorProfile, Notification, DonorResponse


# Blood compatibility matrix - who can donate to whom
BLOOD_COMPATIBILITY = {
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],  # Universal receiver
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+': ['O+', 'O-'],
    'O-': ['O-'],  # Universal donor
}


def get_compatible_blood_groups(requested_blood_group):
    """
    Returns list of blood groups that can donate to the requested blood group.
    
    Args:
        requested_blood_group: The blood group needed (e.g., 'A+')
    
    Returns:
        List of compatible donor blood groups
    """
    return BLOOD_COMPATIBILITY.get(requested_blood_group, [requested_blood_group])


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_staff


@login_required
def home_redirect(request):
    """Redirect user to appropriate page based on their role"""
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('donor_notifications')


@login_required
@user_passes_test(is_staff_user)
@ensure_csrf_cookie
def admin_dashboard(request):
    """Admin dashboard with statistics and all requests"""
    # Get all blood requests
    blood_requests = BloodRequest.objects.all().prefetch_related('responses', 'notifications')
    
    # Get all donors
    donors = DonorProfile.objects.all().select_related('user')
    
    # Calculate statistics
    total_requests = blood_requests.count()
    total_donors = donors.count()
    total_accepted = DonorResponse.objects.filter(response='accepted').count()
    active_requests = blood_requests.filter(is_active=True).count()
    
    context = {
        'blood_requests': blood_requests,
        'donors': donors,
        'total_requests': total_requests,
        'total_donors': total_donors,
        'total_accepted': total_accepted,
        'active_requests': active_requests,
        'blood_groups': DonorProfile.BLOOD_GROUP_CHOICES,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
@ensure_csrf_cookie
@transaction.atomic
def admin_create_request(request):
    """Admin page to create a blood request and notify matching donors with blood compatibility logic"""
    if request.method == 'POST':
        # Debug: Print CSRF token info
        print(f"CSRF Token from POST: {request.POST.get('csrfmiddlewaretoken', 'NOT FOUND')}")
        print(f"CSRF Cookie: {request.COOKIES.get('csrftoken', 'NOT FOUND')}")
        
        blood_group = request.POST.get('blood_group')
        units_needed = request.POST.get('units_needed', 1)
        urgency = request.POST.get('urgency')
        note = request.POST.get('note', '')
        
        # Create the blood request
        blood_request = BloodRequest.objects.create(
            blood_group=blood_group,
            units_needed=units_needed,
            urgency=urgency,
            note=note,
            created_by=request.user
        )
        
        # Get compatible blood groups for the requested blood group
        compatible_blood_groups = get_compatible_blood_groups(blood_group)
        
        # Find ONLY compatible and available donors
        matching_donors = DonorProfile.objects.filter(
            blood_group__in=compatible_blood_groups,
            is_available=True
        ).select_related('user')
        
        # Create notifications for matching donors (wrapped in transaction)
        notifications_created = 0
        for donor_profile in matching_donors:
            try:
                Notification.objects.create(
                    user=donor_profile.user,
                    blood_request=blood_request
                )
                notifications_created += 1
            except IntegrityError:
                # Skip if notification already exists
                pass
        
        messages.success(
            request, 
            f'Blood request created successfully! {notifications_created} compatible donor(s) notified.'
        )
        return redirect('admin_dashboard')
    
    # GET request - show the form
    context = {
        'blood_groups': DonorProfile.BLOOD_GROUP_CHOICES,
        'urgency_levels': BloodRequest.URGENCY_CHOICES,
    }
    return render(request, 'demo_admin_create_request.html', context)


@login_required
@user_passes_test(is_staff_user)
def admin_request_detail(request, request_id):
    """Admin page to view blood request details and accepted donors"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    # Get notified donors count
    notified_count = Notification.objects.filter(blood_request=blood_request).count()
    
    # Get accepted donors with their profiles
    accepted_responses = DonorResponse.objects.filter(
        blood_request=blood_request,
        response='accepted'
    ).select_related('donor', 'donor__donor_profile')
    
    context = {
        'blood_request': blood_request,
        'notified_count': notified_count,
        'accepted_responses': accepted_responses,
    }
    return render(request, 'demo_admin_request_detail.html', context)


@login_required
def donor_notifications(request):
    """Donor page to view their notifications and blood requests"""
    # Check if user has a donor profile
    try:
        donor_profile = DonorProfile.objects.get(user=request.user)
        has_profile = True
    except DonorProfile.DoesNotExist:
        has_profile = False
        donor_profile = None
    
    # Get all notifications for the logged-in user
    notifications = Notification.objects.filter(
        user=request.user
    ).select_related('blood_request').order_by('-created_at')
    
    # Check which requests the donor has already responded to
    responded_request_ids = set(
        DonorResponse.objects.filter(donor=request.user).values_list('blood_request_id', flat=True)
    )
    
    # Add a flag to each notification indicating if responded
    notifications_with_status = []
    for notification in notifications:
        notification.has_responded = notification.blood_request_id in responded_request_ids
        if notification.has_responded:
            response = DonorResponse.objects.get(
                donor=request.user,
                blood_request_id=notification.blood_request_id
            )
            notification.response_status = response.response
        notifications_with_status.append(notification)
    
    context = {
        'notifications': notifications_with_status,
        'user': request.user,
        'has_profile': has_profile,
        'donor_profile': donor_profile,
    }
    return render(request, 'demo_donor_notifications.html', context)


@login_required
@require_http_methods(["POST"])
def donor_respond(request):
    """API endpoint for donor to accept/reject a blood request"""
    try:
        data = json.loads(request.body)
        blood_request_id = data.get('blood_request_id')
        response = data.get('response')
        
        if not blood_request_id or not response:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
        
        if response not in ['accepted', 'rejected']:
            return JsonResponse({'status': 'error', 'message': 'Invalid response value'}, status=400)
        
        blood_request = get_object_or_404(BloodRequest, id=blood_request_id)
        
        # Create or update donor response
        donor_response, created = DonorResponse.objects.update_or_create(
            blood_request=blood_request,
            donor=request.user,
            defaults={'response': response}
        )
        
        # Mark notification as read
        Notification.objects.filter(
            user=request.user,
            blood_request=blood_request
        ).update(is_read=True)
        
        return JsonResponse({
            'status': 'ok',
            'message': f'Response recorded: {response}',
            'created': created
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

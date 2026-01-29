# 🔄 Blood Donation System - Flow Diagrams

## 📊 Complete System Flow

### Overview
```
┌──────────┐     Creates      ┌──────────────┐     Notifies    ┌──────────┐
│  Admin   │ ───────────────> │ BloodRequest │ ─────────────> │  Donors  │
└──────────┘                  └──────────────┘                 └──────────┘
                                      │                               │
                                      │                               │
                                      ▼                               ▼
                              ┌──────────────┐                ┌─────────────┐
                              │ Notification │                │   Respond   │
                              │  (Database)  │                │ Accept/Reject│
                              └──────────────┘                └─────────────┘
                                                                      │
                                                                      ▼
                              ┌──────────────────────────────────────┐
                              │  Admin Views Accepted Donors         │
                              │  (Name, Phone, Blood Group, Time)    │
                              └──────────────────────────────────────┘
```

---

## 1️⃣ Admin Creates Blood Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ ADMIN: Create Blood Request                                     │
└─────────────────────────────────────────────────────────────────┘

Step 1: Admin Login
├─> Navigate to: /accounts/login/
├─> Enter: admin / admin123
├─> Django checks: is_staff = True
└─> Redirect to: /demo/admin/create-request/

Step 2: Fill Form
├─> Select: Blood Group (A+, A-, B+, B-, O+, O-, AB+, AB-)
├─> Enter: Units Needed (1, 2, 3...)
├─> Select: Urgency (Critical, High, Medium)
└─> Enter: Note (optional)

Step 3: Submit (POST)
├─> Django View: admin_create_request()
│   ├─> Create BloodRequest object
│   │   ├─> blood_group = "A+"
│   │   ├─> units_needed = 2
│   │   ├─> urgency = "critical"
│   │   ├─> note = "Urgent surgery tomorrow"
│   │   └─> created_by = current_user
│   │
│   ├─> Query Matching Donors:
│   │   SQL: SELECT * FROM DonorProfile
│   │        WHERE blood_group = "A+"
│   │        AND is_available = True
│   │   Result: [john_donor, sarah_donor]
│   │
│   ├─> Create Notifications:
│   │   FOR EACH donor IN matching_donors:
│   │       Create Notification(
│   │           user = donor.user,
│   │           blood_request = blood_request
│   │       )
│   │   Result: 2 notifications created
│   │
│   └─> Show Success Message:
│       "Blood request created successfully! 2 donors notified."
│
└─> Redirect to: /demo/admin/request/<id>/

Step 4: View Results
├─> Show Request Details
│   ├─> Blood Group: A+
│   ├─> Units: 2
│   ├─> Urgency: Critical
│   └─> Note: "Urgent surgery tomorrow"
│
├─> Show Statistics
│   ├─> Notified Donors: 2
│   └─> Accepted Donors: 0 (initially)
│
└─> Show Accepted Donors Table: [Empty initially]
```

---

## 2️⃣ Donor Views Notifications Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ DONOR: View Notifications                                       │
└─────────────────────────────────────────────────────────────────┘

Step 1: Donor Login
├─> Navigate to: /accounts/login/
├─> Enter: john_donor / donor123
├─> Django checks: user.is_authenticated = True
└─> Redirect to: /demo/donor/notifications/

Step 2: Load Notifications
├─> Django View: donor_notifications()
│   ├─> Query Notifications:
│   │   SQL: SELECT * FROM Notification
│   │        WHERE user_id = current_user.id
│   │        ORDER BY created_at DESC
│   │   Result: [Notification #1]
│   │
│   ├─> Join with BloodRequest:
│   │   Get blood_group, units, urgency, note
│   │
│   ├─> Check if Already Responded:
│   │   SQL: SELECT * FROM DonorResponse
│   │        WHERE donor_id = current_user.id
│   │        AND blood_request_id = X
│   │   Result: None (not responded yet)
│   │
│   └─> Add Flag: has_responded = False
│
└─> Render Template with Notifications

Step 3: Display Notification Card
├─> Card Header:
│   ├─> Title: "Blood Request #1"
│   └─> Badge: "Critical Priority" (red, pulsing)
│
├─> Card Body:
│   ├─> Blood Group: A+ (red, large)
│   ├─> Units Needed: 2
│   ├─> Created: Jan 21, 2026 10:30 AM
│   └─> Note: "Urgent surgery tomorrow"
│
└─> Card Actions:
    ├─> Button: "Accept & Donate" (green)
    └─> Button: "Can't Donate" (red)
```

---

## 3️⃣ Donor Responds (Accept/Reject) Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ DONOR: Accept/Reject Request                                    │
└─────────────────────────────────────────────────────────────────┘

Step 1: User Clicks "Accept & Donate"
├─> JavaScript Event:
│   onclick="respondToRequest(1, 'accepted')"
│
└─> JavaScript Function Executes:
    ├─> Disable buttons immediately
    ├─> Change text to "Processing..."
    └─> Prepare AJAX request

Step 2: JavaScript Fetch API Call
├─> Get CSRF Token:
│   const csrftoken = getCookie('csrftoken');
│
├─> Prepare Request:
│   URL: /demo/donor/respond/
│   Method: POST
│   Headers: {
│       'Content-Type': 'application/json',
│       'X-CSRFToken': csrftoken
│   }
│   Body: {
│       "blood_request_id": 1,
│       "response": "accepted"
│   }
│
└─> Send Request (async)

Step 3: Django Backend Processing
├─> View: donor_respond()
│   ├─> Parse JSON Body
│   ├─> Validate:
│   │   ├─> blood_request_id exists?
│   │   ├─> response is "accepted" or "rejected"?
│   │   └─> User is authenticated?
│   │
│   ├─> Create/Update DonorResponse:
│   │   DonorResponse.objects.update_or_create(
│   │       blood_request_id = 1,
│   │       donor_id = current_user.id,
│   │       defaults = {'response': 'accepted'}
│   │   )
│   │   ├─> Check unique constraint (blood_request, donor)
│   │   └─> Result: DonorResponse created
│   │
│   ├─> Mark Notification as Read:
│   │   Notification.objects.filter(
│   │       user = current_user,
│   │       blood_request_id = 1
│   │   ).update(is_read = True)
│   │
│   └─> Return JSON Response:
│       {
│           "status": "ok",
│           "message": "Response recorded: accepted",
│           "created": true
│       }
│
└─> Response sent to JavaScript

Step 4: JavaScript Updates UI
├─> Receive JSON Response
│   ├─> data.status === "ok"
│   └─> data.message === "Response recorded: accepted"
│
├─> Update UI (NO PAGE RELOAD):
│   ├─> Remove buttons
│   ├─> Show: "✓ You accepted this request" (green box)
│   ├─> Add class "responded" to card (faded)
│   └─> Show alert: "Response recorded: accepted"
│
└─> User sees confirmation instantly
```

---

## 4️⃣ Admin Views Accepted Donors Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ ADMIN: View Accepted Donors                                     │
└─────────────────────────────────────────────────────────────────┘

Step 1: Admin Navigates to Request Detail
├─> Login as admin
└─> Navigate to: /demo/admin/request/1/

Step 2: Django Backend Query
├─> View: admin_request_detail(request_id=1)
│   ├─> Get BloodRequest:
│   │   blood_request = BloodRequest.objects.get(id=1)
│   │
│   ├─> Count Notified Donors:
│   │   notified_count = Notification.objects.filter(
│   │       blood_request_id = 1
│   │   ).count()
│   │   Result: 2
│   │
│   └─> Get Accepted Donors:
│       accepted_responses = DonorResponse.objects.filter(
│           blood_request_id = 1,
│           response = 'accepted'
│       ).select_related('donor', 'donor__donor_profile')
│       Result: [DonorResponse(donor=john_donor, ...)]
│
└─> Render Template

Step 3: Display Results
├─> Request Information:
│   ├─> Request ID: #1
│   ├─> Blood Group: A+
│   ├─> Units: 2
│   ├─> Urgency: Critical (red badge)
│   ├─> Created By: admin
│   ├─> Created At: Jan 21, 2026 10:30 AM
│   └─> Note: "Urgent surgery tomorrow"
│
├─> Statistics Cards:
│   ├─> Notified Donors: 2
│   └─> Accepted Donors: 1
│
└─> Accepted Donors Table:
    ┌──────────────┬──────────────┬────────────┬────────────────┐
    │ Username     │ Phone        │ Blood Group│ Responded At   │
    ├──────────────┼──────────────┼────────────┼────────────────┤
    │ john_donor   │ +1234567890  │ A+         │ Jan 21, 10:35  │
    └──────────────┴──────────────┴────────────┴────────────────┘

Step 4: Admin Actions
├─> Admin can see donor contact information
├─> Admin can call donor: +1234567890
└─> Admin can create another request
```

---

## 5️⃣ Duplicate Response Prevention Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ SYSTEM: Prevent Duplicate Responses                             │
└─────────────────────────────────────────────────────────────────┘

Scenario: Donor tries to respond twice

Step 1: Initial Response
├─> john_donor accepts Request #1
├─> DonorResponse created:
│   ├─> blood_request_id = 1
│   ├─> donor_id = john_donor.id
│   └─> response = 'accepted'
└─> UI shows: "✓ You accepted this request"

Step 2: Donor Refreshes Page
├─> GET /demo/donor/notifications/
├─> Django queries:
│   responded_request_ids = DonorResponse.objects.filter(
│       donor = current_user
│   ).values_list('blood_request_id', flat=True)
│   Result: [1]
│
├─> For each notification:
│   notification.has_responded = (
│       notification.blood_request_id in responded_request_ids
│   )
│   Result: True for Request #1
│
└─> Template shows: "✓ You accepted this request"
    (Buttons NOT shown)

Step 3: If Donor Tries to Click Again (Impossible)
├─> Buttons are not rendered in template
├─> UI prevents click
└─> No API call made

Step 4: If Someone Bypasses Frontend
├─> POST /demo/donor/respond/
│   Body: {"blood_request_id": 1, "response": "rejected"}
│
├─> Django tries to create:
│   DonorResponse.objects.update_or_create(
│       blood_request_id = 1,
│       donor_id = john_donor.id,
│       defaults = {'response': 'rejected'}
│   )
│
├─> Database Constraint Check:
│   UNIQUE (blood_request_id, donor_id)
│   Record exists: (1, john_donor.id) ← CONFLICT
│
└─> Result: Updates existing record instead of creating duplicate
    Old: response='accepted'
    New: response='rejected'
    (This is intentional - allows changing response)
```

---

## 6️⃣ Blood Group Matching Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ SYSTEM: Blood Group Matching Logic                              │
└─────────────────────────────────────────────────────────────────┘

Database State:
┌──────────────┬─────────────┬──────────────┐
│ Username     │ Blood Group │ Is Available │
├──────────────┼─────────────┼──────────────┤
│ john_donor   │ A+          │ True         │
│ sarah_donor  │ A+          │ True         │
│ mike_donor   │ O+          │ True         │
│ lisa_donor   │ B+          │ True         │
└──────────────┴─────────────┴──────────────┘

Scenario 1: Admin creates A+ request
├─> Query: blood_group='A+' AND is_available=True
├─> Match: john_donor, sarah_donor ✓
├─> No Match: mike_donor (O+), lisa_donor (B+)
└─> Result: 2 notifications created

Scenario 2: Admin creates O+ request
├─> Query: blood_group='O+' AND is_available=True
├─> Match: mike_donor ✓
├─> No Match: john_donor, sarah_donor, lisa_donor
└─> Result: 1 notification created

Scenario 3: Admin creates B+ request
├─> Query: blood_group='B+' AND is_available=True
├─> Match: lisa_donor ✓
├─> No Match: john_donor, sarah_donor, mike_donor
└─> Result: 1 notification created

Scenario 4: Donor is unavailable
├─> lisa_donor sets is_available = False
├─> Admin creates B+ request
├─> Query: blood_group='B+' AND is_available=True
├─> Match: None (lisa_donor is unavailable)
└─> Result: 0 notifications created
```

---

## 7️⃣ Authentication & Authorization Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ SYSTEM: Security & Access Control                               │
└─────────────────────────────────────────────────────────────────┘

User tries to access: /demo/admin/create-request/

Step 1: Check if Authenticated
├─> Django Middleware: AuthenticationMiddleware
├─> Check session: sessionid cookie exists?
│   ├─> YES: User is logged in
│   └─> NO: Redirect to /accounts/login/?next=/demo/admin/create-request/
│
└─> @login_required decorator

Step 2: Check if Staff
├─> Django checks: user.is_staff == True?
│   ├─> YES: Allow access
│   └─> NO: Show 403 Forbidden or redirect
│
└─> @user_passes_test(is_staff_user) decorator

Step 3: Access Granted
├─> User can create blood requests
└─> User can view request details

---

User tries to access: /demo/donor/notifications/

Step 1: Check if Authenticated
├─> @login_required decorator
│   ├─> YES: Allow access
│   └─> NO: Redirect to login
│
└─> No is_staff check (any authenticated user)

Step 2: Filter by User
├─> notifications = Notification.objects.filter(user=request.user)
├─> Only shows current user's notifications
└─> Cannot see other donors' notifications

---

User tries to respond: POST /demo/donor/respond/

Step 1: Authentication Check
├─> @login_required decorator
│   ├─> YES: Continue
│   └─> NO: Return 401 Unauthorized
│
Step 2: CSRF Check
├─> Django Middleware: CsrfViewMiddleware
├─> Check X-CSRFToken header
│   ├─> Valid: Continue
│   └─> Invalid: Return 403 Forbidden
│
Step 3: Authorization Check
├─> Donor can only respond for themselves
├─> System automatically uses request.user
└─> Cannot respond on behalf of another donor
```

---

## 8️⃣ Complete Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐              ┌─────────────────┐           │
│  │  Admin Pages    │              │  Donor Pages    │           │
│  │                 │              │                 │           │
│  │ • Create Request│              │ • Notifications │           │
│  │ • View Details  │              │ • Accept/Reject │           │
│  └────────┬────────┘              └────────┬────────┘           │
│           │                                │                     │
└───────────┼────────────────────────────────┼─────────────────────┘
            │                                │
            │ HTTP GET/POST                  │ HTTP + AJAX
            │                                │
┌───────────▼────────────────────────────────▼─────────────────────┐
│                       DJANGO VIEWS LAYER                          │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  admin_create_request()          donor_notifications()           │
│         │                                 │                       │
│         ├─> Validate form                ├─> Get user notifs     │
│         ├─> Create BloodRequest          ├─> Check responses     │
│         ├─> Find matching donors         └─> Render template     │
│         ├─> Create notifications                                 │
│         └─> Redirect                                              │
│                                                                   │
│  admin_request_detail()          donor_respond() [JSON API]      │
│         │                                 │                       │
│         ├─> Get request                  ├─> Parse JSON          │
│         ├─> Count notified               ├─> Create response     │
│         ├─> Get accepted                 ├─> Mark read           │
│         └─> Render template              └─> Return JSON         │
│                                                                   │
└───────────┬──────────────────────────────┬────────────────────────┘
            │                              │
            │ Django ORM                   │ Django ORM
            │                              │
┌───────────▼──────────────────────────────▼────────────────────────┐
│                      DJANGO MODELS LAYER                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │DonorProfile  │  │ BloodRequest │  │ Notification │           │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤           │
│  │• user        │  │• blood_group │  │• user        │           │
│  │• phone       │  │• units       │  │• request     │           │
│  │• blood_group │  │• urgency     │  │• is_read     │           │
│  │• is_available│  │• note        │  └──────────────┘           │
│  └──────────────┘  └──────────────┘                              │
│                                                                    │
│  ┌──────────────┐                                                │
│  │DonorResponse │                                                │
│  ├──────────────┤                                                │
│  │• request     │                                                │
│  │• donor       │                                                │
│  │• response    │                                                │
│  └──────────────┘                                                │
│                                                                    │
└────────────┬───────────────────────────────────────────────────────┘
             │
             │ SQL Queries
             │
┌────────────▼───────────────────────────────────────────────────────┐
│                        DATABASE (SQLite)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Tables:                                                            │
│  • auth_user                                                        │
│  • careapp_donorprofile                                            │
│  • careapp_bloodrequest                                            │
│  • careapp_notification (unique: user + request)                   │
│  • careapp_donorresponse (unique: donor + request)                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Decision Points

### When to Notify Donors?
```
Trigger: BloodRequest created
Action: Immediately query and create Notification rows
Condition: blood_group matches AND is_available = True
```

### When to Show Buttons?
```
Check: Has donor already responded?
YES → Show: "✓ You accepted/rejected this request"
NO  → Show: Accept & Reject buttons
```

### When to Update UI?
```
Method: JavaScript fetch() with JSON response
Timing: Immediately after successful API response
Effect: No page reload, instant feedback
```

### When to Prevent Duplicates?
```
Level 1: Frontend - Don't show buttons if responded
Level 2: Backend - unique_together constraint
Level 3: Logic - update_or_create allows response change
```

---

This flow diagram shows exactly how data moves through your system from user action to database and back. Each step is implemented and working in your code! 🚀

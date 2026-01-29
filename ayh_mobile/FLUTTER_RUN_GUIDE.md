# Flutter App - Quick Run Guide

## ✅ Complete! All Files Created

### 📁 Project Structure Created:
```
lib/
├── core/
│   ├── api/
│   │   └── api_client.dart          ✅ Dio HTTP client with interceptors
│   └── constants/
│       ├── api_constants.dart        ✅ All API endpoints
│       └── app_colors.dart           ✅ Color theme
│
├── data/
│   ├── models/
│   │   ├── user.dart                 ✅ User model
│   │   ├── donor_profile.dart        ✅ Donor profile model
│   │   ├── blood_request.dart        ✅ Blood request model
│   │   ├── notification.dart         ✅ Notification model
│   │   └── dashboard_stats.dart      ✅ Dashboard stats model
│   │
│   ├── services/
│   │   ├── storage_service.dart      ✅ Token & data storage
│   │   ├── auth_service.dart         ✅ Auth API calls
│   │   ├── donor_service.dart        ✅ Donor API calls
│   │   ├── blood_request_service.dart ✅ Blood request API calls
│   │   ├── notification_service.dart  ✅ Notification API calls
│   │   ├── response_service.dart      ✅ Response API calls
│   │   └── dashboard_service.dart     ✅ Dashboard API calls
│   │
│   └── repositories/
│       ├── auth_repository.dart       ✅ Auth business logic
│       ├── donor_repository.dart      ✅ Donor business logic
│       ├── blood_request_repository.dart ✅ Request business logic
│       ├── notification_repository.dart  ✅ Notification business logic
│       └── dashboard_repository.dart     ✅ Dashboard business logic
│
├── presentation/
│   ├── providers/
│   │   ├── auth_provider.dart         ✅ Auth state management
│   │   ├── donor_provider.dart        ✅ Donor state management
│   │   ├── blood_request_provider.dart ✅ Request state management
│   │   ├── notification_provider.dart  ✅ Notification state management
│   │   └── dashboard_provider.dart     ✅ Dashboard state management
│   │
│   └── screens/
│       ├── auth/
│       │   ├── login_screen.dart       ✅ Login UI
│       │   └── register_screen.dart    ✅ Register UI
│       │
│       ├── donor/
│       │   ├── create_profile_screen.dart ✅ Create donor profile UI
│       │   └── donor_home_screen.dart     ✅ Donor notifications UI
│       │
│       └── admin/
│           ├── admin_dashboard_screen.dart ✅ Admin dashboard UI
│           └── create_request_screen.dart  ✅ Create blood request UI
│
└── main.dart                          ✅ App entry point
```

---

## 🚀 How to Run

### Step 1: Start Django Backend
```bash
cd C:\Users\Avs-Mohandas\Desktop\Projects\AYH\AYH
python manage.py runserver
```

**Backend will run on:** `http://127.0.0.1:8000`

### Step 2: Run Flutter App
```bash
cd C:\Users\Avs-Mohandas\Desktop\Projects\AYH\ayh_mobile
flutter run
```

---

## 📱 Test Flow

### As Admin:
1. Open Flutter app
2. Login with: `admin` / `admin123`
3. You'll see Admin Dashboard with statistics
4. Click "Create Request" button (bottom right)
5. Fill form:
   - Blood Group: Select any (e.g., A+)
   - Units: Enter 1-10
   - Urgency: Select (Critical/High/Medium)
   - Note: Optional text
6. Click "Create Request"
7. Django will automatically notify compatible donors

### As Donor:
1. Open Flutter app (or logout and login again)
2. Login with: `john_donor` / `donor123`
3. You'll see Donor Home screen with notifications
4. If you see notification:
   - Click "Accept & Donate" to accept
   - Click "Can't Donate" to reject
5. Response sent to Django backend
6. Admin can now see your acceptance

---

## 🔧 API Connection

The app automatically detects your platform:

- **Android Emulator**: Uses `http://10.0.2.2:8000/api/`
- **iOS Simulator**: Uses `http://localhost:8000/api/`
- **Physical Device**: Uses `http://192.168.1.100:8000/api/` (update your local IP)

**To change IP for physical device:**
Edit: `lib/core/constants/api_constants.dart` line 13

---

## 🎨 Features Implemented

### ✅ Authentication:
- Login with JWT tokens
- Register new users
- Auto token refresh
- Secure token storage
- Logout

### ✅ Admin Features:
- Dashboard with statistics
- Create blood requests
- View all requests
- Auto-notification to compatible donors
- Pull to refresh

### ✅ Donor Features:
- View notifications
- Accept/Reject requests
- See donation history
- Create donor profile
- Update availability

### ✅ API Integration:
- All 23 Django endpoints connected
- Automatic token management
- Error handling
- Loading states
- Success/error messages

---

## 🧪 Testing

### Create Test Scenario:

1. **Start Backend:**
   ```bash
   python manage.py runserver
   ```

2. **Run Flutter (Admin):**
   - Login as admin
   - Create blood request for A+
   - See "X donors notified" message

3. **Run Flutter (Donor):**
   - Login as donor with A+, A-, O+, or O- blood type
   - See notification appear
   - Accept the request

4. **Back to Admin:**
   - Refresh dashboard
   - See "1 accepted" in the request card

---

## 📝 Key Files for Customization

### Change API URL:
`lib/core/constants/api_constants.dart`

### Change Colors:
`lib/core/constants/app_colors.dart`

### Add New API Endpoint:
1. Add constant in `api_constants.dart`
2. Create method in appropriate service
3. Add to repository
4. Use in provider
5. Call from UI screen

---

## 🐛 Troubleshooting

### "Connection refused" error:
- Make sure Django is running
- Check if you're using correct IP
- For Android emulator, use `10.0.2.2`

### "Invalid credentials":
- Check username/password
- Test credentials: admin/admin123 or john_donor/donor123

### Packages not found:
```bash
flutter pub get
```

### Build errors:
```bash
flutter clean
flutter pub get
flutter run
```

---

## 📦 Dependencies Used

- `dio`: HTTP client
- `provider`: State management
- `flutter_secure_storage`: Secure token storage
- `shared_preferences`: Local data storage

All already installed! ✅

---

## 🎯 What's Working

✅ Login/Register/Logout  
✅ JWT token authentication  
✅ Auto token refresh  
✅ Admin dashboard with stats  
✅ Create blood requests  
✅ Donor notifications  
✅ Accept/Reject requests  
✅ Blood compatibility matching  
✅ Real-time data sync  
✅ Error handling  
✅ Loading states  
✅ Pull to refresh  

**Everything connects to your Django API!** 🚀

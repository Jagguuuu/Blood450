import 'dart:io';

class ApiConstants {
  // Base URL - Auto-detect platform
  static String get baseUrl {
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000/api/';
    } else if (Platform.isIOS) {
      return 'http://localhost:8000/api/';
    } else {
      return 'http://192.168.1.100:8000/api/';
    }
  }

  // Authentication endpoints
  static const String login = 'auth/login/';
  static const String register = 'auth/register/';
  static const String logout = 'auth/logout/';
  static const String currentUser = 'auth/me/';
  static const String tokenRefresh = 'auth/token/refresh/';

  // Donor profile endpoints
  static const String donors = 'donors/';
  static const String donorMe = 'donors/me/';
  static const String donorUpdateMe = 'donors/update_me/';

  // Blood request endpoints
  static const String bloodRequests = 'blood-requests/';
  static const String bloodRequestsActive = 'blood-requests/active/';
  static const String bloodRequestsMyRequests = 'blood-requests/my_requests/';

  // Notification endpoints
  static const String notifications = 'notifications/';
  static const String notificationMarkAllRead = 'notifications/mark_all_read/';

  // Response endpoint
  static const String respond = 'respond/';

  // Dashboard endpoint
  static const String dashboard = 'dashboard/';
}

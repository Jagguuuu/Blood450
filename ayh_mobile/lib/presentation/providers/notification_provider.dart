import 'package:flutter/foundation.dart';
import '../../data/repositories/notification_repository.dart';
import '../../data/models/notification.dart';

class NotificationProvider with ChangeNotifier {
  final NotificationRepository _repository = NotificationRepository();

  List<NotificationModel> _notifications = [];
  bool _isLoading = false;
  String? _error;

  List<NotificationModel> get notifications => _notifications;
  bool get isLoading => _isLoading;
  String? get error => _error;
  
  int get unreadCount => _notifications.where((n) => !n.isRead).length;
  List<NotificationModel> get unreadNotifications => 
      _notifications.where((n) => !n.isRead).toList();

  Future<void> loadNotifications() async {
    _isLoading = true;
    notifyListeners();

    try {
      _notifications = await _repository.getMyNotifications();
      _error = null;
    } catch (e) {
      _error = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<bool> markAsRead(int id) async {
    final success = await _repository.markAsRead(id);
    if (success) {
      final index = _notifications.indexWhere((n) => n.id == id);
      if (index != -1) {
        _notifications[index] = NotificationModel(
          id: _notifications[index].id,
          bloodRequest: _notifications[index].bloodRequest,
          isRead: true,
          createdAt: _notifications[index].createdAt,
          hasResponded: _notifications[index].hasResponded,
          responseStatus: _notifications[index].responseStatus,
        );
        notifyListeners();
      }
    }
    return success;
  }

  Future<bool> markAllAsRead() async {
    final success = await _repository.markAllAsRead();
    if (success) {
      await loadNotifications();
    }
    return success;
  }

  Future<Map<String, dynamic>> respondToRequest({
    required int bloodRequestId,
    required String response,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await _repository.respondToRequest(
        bloodRequestId: bloodRequestId,
        response: response,
      );
      
      if (result['success']) {
        // Reload notifications to update status
        await loadNotifications();
      } else {
        _error = result['error'];
      }
      
      _isLoading = false;
      notifyListeners();
      return result;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return {'success': false, 'error': e.toString()};
    }
  }
}

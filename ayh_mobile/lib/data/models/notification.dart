import 'blood_request.dart';

class NotificationModel {
  final int id;
  final BloodRequest bloodRequest;
  final bool isRead;
  final DateTime createdAt;
  final bool hasResponded;
  final String? responseStatus;

  NotificationModel({
    required this.id,
    required this.bloodRequest,
    required this.isRead,
    required this.createdAt,
    required this.hasResponded,
    this.responseStatus,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      id: json['id'] ?? 0,
      bloodRequest: BloodRequest.fromJson(json['blood_request'] ?? {}),
      isRead: json['is_read'] ?? false,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
      hasResponded: json['has_responded'] ?? false,
      responseStatus: json['response_status'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'is_read': isRead,
      'has_responded': hasResponded,
      'response_status': responseStatus,
    };
  }
}

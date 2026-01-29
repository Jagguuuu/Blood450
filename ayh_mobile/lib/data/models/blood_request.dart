import 'user.dart';

class BloodRequest {
  final int id;
  final String bloodGroup;
  final int unitsNeeded;
  final String urgency;
  final String urgencyDisplay;
  final String note;
  final int? createdBy;
  final String? createdByUsername;
  final bool isActive;
  final DateTime createdAt;
  final int notifiedCount;
  final int acceptedCount;
  final User? createdByUser;
  final List<NotifiedDonor>? notifiedDonors;
  final List<AcceptedDonor>? acceptedDonors;

  BloodRequest({
    required this.id,
    required this.bloodGroup,
    required this.unitsNeeded,
    required this.urgency,
    required this.urgencyDisplay,
    required this.note,
    this.createdBy,
    this.createdByUsername,
    required this.isActive,
    required this.createdAt,
    required this.notifiedCount,
    required this.acceptedCount,
    this.createdByUser,
    this.notifiedDonors,
    this.acceptedDonors,
  });

  factory BloodRequest.fromJson(Map<String, dynamic> json) {
    return BloodRequest(
      id: json['id'] ?? 0,
      bloodGroup: json['blood_group'] ?? '',
      unitsNeeded: json['units_needed'] ?? 1,
      urgency: json['urgency'] ?? '',
      urgencyDisplay: json['urgency_display'] ?? json['urgency'] ?? '',
      note: json['note'] ?? '',
      createdBy: json['created_by'],
      createdByUsername: json['created_by_username'],
      isActive: json['is_active'] ?? true,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
      notifiedCount: json['notified_count'] ?? 0,
      acceptedCount: json['accepted_count'] ?? 0,
      createdByUser: json['created_by'] != null && json['created_by'] is Map
          ? User.fromJson(json['created_by'])
          : null,
      notifiedDonors: json['notified_donors'] != null
          ? (json['notified_donors'] as List)
              .map((d) => NotifiedDonor.fromJson(d))
              .toList()
          : null,
      acceptedDonors: json['accepted_donors'] != null
          ? (json['accepted_donors'] as List)
              .map((d) => AcceptedDonor.fromJson(d))
              .toList()
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'blood_group': bloodGroup,
      'units_needed': unitsNeeded,
      'urgency': urgency,
      'note': note,
      'is_active': isActive,
    };
  }
}

class NotifiedDonor {
  final int id;
  final String username;
  final String? bloodGroup;
  final DateTime notifiedAt;

  NotifiedDonor({
    required this.id,
    required this.username,
    this.bloodGroup,
    required this.notifiedAt,
  });

  factory NotifiedDonor.fromJson(Map<String, dynamic> json) {
    return NotifiedDonor(
      id: json['id'] ?? 0,
      username: json['username'] ?? '',
      bloodGroup: json['blood_group'],
      notifiedAt: json['notified_at'] != null
          ? DateTime.parse(json['notified_at'])
          : DateTime.now(),
    );
  }
}

class AcceptedDonor {
  final int id;
  final String username;
  final String? phone;
  final String? bloodGroup;
  final DateTime respondedAt;

  AcceptedDonor({
    required this.id,
    required this.username,
    this.phone,
    this.bloodGroup,
    required this.respondedAt,
  });

  factory AcceptedDonor.fromJson(Map<String, dynamic> json) {
    return AcceptedDonor(
      id: json['id'] ?? 0,
      username: json['username'] ?? '',
      phone: json['phone'],
      bloodGroup: json['blood_group'],
      respondedAt: json['responded_at'] != null
          ? DateTime.parse(json['responded_at'])
          : DateTime.now(),
    );
  }
}

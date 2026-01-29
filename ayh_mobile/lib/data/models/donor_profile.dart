import 'user.dart';

class DonorProfile {
  final int id;
  final User? user;
  final String username;
  final String phone;
  final String bloodGroup;
  final bool isAvailable;
  final DateTime createdAt;

  DonorProfile({
    required this.id,
    this.user,
    required this.username,
    required this.phone,
    required this.bloodGroup,
    required this.isAvailable,
    required this.createdAt,
  });

  factory DonorProfile.fromJson(Map<String, dynamic> json) {
    return DonorProfile(
      id: json['id'] ?? 0,
      user: json['user'] != null ? User.fromJson(json['user']) : null,
      username: json['username'] ?? '',
      phone: json['phone'] ?? '',
      bloodGroup: json['blood_group'] ?? '',
      isAvailable: json['is_available'] ?? true,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'phone': phone,
      'blood_group': bloodGroup,
      'is_available': isAvailable,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

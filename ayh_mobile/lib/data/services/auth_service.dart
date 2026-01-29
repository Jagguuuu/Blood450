import '../../core/api/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../models/user.dart';
import '../models/donor_profile.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.login,
        data: {
          'username': username,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        return {
          'success': true,
          'access': data['access'],
          'refresh': data['refresh'],
          'user': User.fromJson(data['user']),
          'has_donor_profile': data['has_donor_profile'] ?? false,
          'donor_profile': data['donor_profile'] != null
              ? DonorProfile.fromJson(data['donor_profile'])
              : null,
        };
      }
      return {'success': false, 'error': 'Login failed'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }

  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String password,
    required String passwordConfirm,
    String? firstName,
    String? lastName,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.register,
        data: {
          'username': username,
          'email': email,
          'password': password,
          'password_confirm': passwordConfirm,
          'first_name': firstName ?? '',
          'last_name': lastName ?? '',
        },
      );

      if (response.statusCode == 201) {
        final data = response.data;
        return {
          'success': true,
          'access': data['access'],
          'refresh': data['refresh'],
          'user': User.fromJson(data['user']),
          'message': data['message'],
        };
      }
      return {'success': false, 'error': 'Registration failed'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }

  Future<Map<String, dynamic>> getCurrentUser() async {
    try {
      final response = await _apiClient.get(ApiConstants.currentUser);

      if (response.statusCode == 200) {
        final data = response.data;
        return {
          'success': true,
          'user': User.fromJson(data['user']),
          'has_donor_profile': data['has_donor_profile'] ?? false,
          'donor_profile': data['donor_profile'] != null
              ? DonorProfile.fromJson(data['donor_profile'])
              : null,
        };
      }
      return {'success': false, 'error': 'Failed to get user'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }

  Future<bool> logout(String refreshToken) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.logout,
        data: {'refresh': refreshToken},
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

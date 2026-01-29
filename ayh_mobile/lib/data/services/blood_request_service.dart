import '../../core/api/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../models/blood_request.dart';

class BloodRequestService {
  final ApiClient _apiClient = ApiClient();

  Future<List<BloodRequest>> getAllRequests() async {
    try {
      final response = await _apiClient.get(ApiConstants.bloodRequests);
      if (response.statusCode == 200) {
        return (response.data as List)
            .map((json) => BloodRequest.fromJson(json))
            .toList();
      }
      return [];
    } catch (e) {
      print('Error getting requests: $e');
      return [];
    }
  }

  Future<List<BloodRequest>> getActiveRequests() async {
    try {
      final response = await _apiClient.get(ApiConstants.bloodRequestsActive);
      if (response.statusCode == 200) {
        return (response.data as List)
            .map((json) => BloodRequest.fromJson(json))
            .toList();
      }
      return [];
    } catch (e) {
      print('Error getting active requests: $e');
      return [];
    }
  }

  Future<List<BloodRequest>> getMyRequests() async {
    try {
      final response = await _apiClient.get(ApiConstants.bloodRequestsMyRequests);
      if (response.statusCode == 200) {
        return (response.data as List)
            .map((json) => BloodRequest.fromJson(json))
            .toList();
      }
      return [];
    } catch (e) {
      print('Error getting my requests: $e');
      return [];
    }
  }

  Future<BloodRequest?> getRequestDetail(int id) async {
    try {
      final response = await _apiClient.get('${ApiConstants.bloodRequests}$id/');
      if (response.statusCode == 200) {
        return BloodRequest.fromJson(response.data);
      }
      return null;
    } catch (e) {
      print('Error getting request detail: $e');
      return null;
    }
  }

  Future<Map<String, dynamic>> createRequest({
    required String bloodGroup,
    required int unitsNeeded,
    required String urgency,
    String? note,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.bloodRequests,
        data: {
          'blood_group': bloodGroup,
          'units_needed': unitsNeeded,
          'urgency': urgency,
          'note': note ?? '',
        },
      );

      if (response.statusCode == 201) {
        return {
          'success': true,
          'message': response.data['message'],
          'blood_request': BloodRequest.fromJson(response.data['blood_request']),
        };
      }
      return {'success': false, 'error': 'Failed to create request'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }

  Future<bool> updateRequest(int id, {bool? isActive}) async {
    try {
      final response = await _apiClient.put(
        '${ApiConstants.bloodRequests}$id/',
        data: {'is_active': isActive},
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Error updating request: $e');
      return false;
    }
  }

  Future<bool> deleteRequest(int id) async {
    try {
      final response = await _apiClient.delete('${ApiConstants.bloodRequests}$id/');
      return response.statusCode == 204;
    } catch (e) {
      print('Error deleting request: $e');
      return false;
    }
  }
}

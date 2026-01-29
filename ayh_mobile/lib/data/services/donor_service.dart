import '../../core/api/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../models/donor_profile.dart';

class DonorService {
  final ApiClient _apiClient = ApiClient();

  Future<DonorProfile?> getMyProfile() async {
    try {
      final response = await _apiClient.get(ApiConstants.donorMe);
      if (response.statusCode == 200) {
        return DonorProfile.fromJson(response.data);
      }
      return null;
    } catch (e) {
      print('Error getting profile: $e');
      return null;
    }
  }

  Future<DonorProfile?> createProfile({
    required String phone,
    required String bloodGroup,
    required bool isAvailable,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.donors,
        data: {
          'phone': phone,
          'blood_group': bloodGroup,
          'is_available': isAvailable,
        },
      );

      if (response.statusCode == 201) {
        return DonorProfile.fromJson(response.data);
      }
      return null;
    } catch (e) {
      print('Error creating profile: $e');
      return null;
    }
  }

  Future<DonorProfile?> updateMyProfile({
    String? phone,
    String? bloodGroup,
    bool? isAvailable,
  }) async {
    try {
      final data = <String, dynamic>{};
      if (phone != null) data['phone'] = phone;
      if (bloodGroup != null) data['blood_group'] = bloodGroup;
      if (isAvailable != null) data['is_available'] = isAvailable;

      final response = await _apiClient.put(
        ApiConstants.donorUpdateMe,
        data: data,
      );

      if (response.statusCode == 200) {
        return DonorProfile.fromJson(response.data);
      }
      return null;
    } catch (e) {
      print('Error updating profile: $e');
      return null;
    }
  }

  Future<List<DonorProfile>> getAllDonors() async {
    try {
      final response = await _apiClient.get(ApiConstants.donors);
      if (response.statusCode == 200) {
        return (response.data as List)
            .map((json) => DonorProfile.fromJson(json))
            .toList();
      }
      return [];
    } catch (e) {
      print('Error getting donors: $e');
      return [];
    }
  }
}

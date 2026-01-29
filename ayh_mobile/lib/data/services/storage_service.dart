import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../models/user.dart';
import '../models/donor_profile.dart';

class StorageService {
  static final StorageService _instance = StorageService._internal();
  factory StorageService() => _instance;

  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  SharedPreferences? _prefs;

  StorageService._internal();

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // Token management
  Future<void> saveTokens(String accessToken, String refreshToken) async {
    await _secureStorage.write(key: 'access_token', value: accessToken);
    await _secureStorage.write(key: 'refresh_token', value: refreshToken);
  }

  Future<String?> getAccessToken() async {
    return await _secureStorage.read(key: 'access_token');
  }

  Future<String?> getRefreshToken() async {
    return await _secureStorage.read(key: 'refresh_token');
  }

  Future<void> clearTokens() async {
    await _secureStorage.deleteAll();
  }

  // User data
  Future<void> saveUser(User user) async {
    await _prefs?.setString('user', json.encode(user.toJson()));
  }

  Future<User?> getUser() async {
    String? userJson = _prefs?.getString('user');
    if (userJson != null) {
      return User.fromJson(json.decode(userJson));
    }
    return null;
  }

  Future<void> clearUser() async {
    await _prefs?.remove('user');
  }

  // Donor profile
  Future<void> saveDonorProfile(DonorProfile profile) async {
    await _prefs?.setString('donor_profile', json.encode(profile.toJson()));
  }

  Future<DonorProfile?> getDonorProfile() async {
    String? profileJson = _prefs?.getString('donor_profile');
    if (profileJson != null) {
      return DonorProfile.fromJson(json.decode(profileJson));
    }
    return null;
  }

  Future<void> clearDonorProfile() async {
    await _prefs?.remove('donor_profile');
  }

  // Clear all data
  Future<void> clearAll() async {
    await clearTokens();
    await clearUser();
    await clearDonorProfile();
  }

  // Check if logged in
  Future<bool> isLoggedIn() async {
    String? token = await getAccessToken();
    return token != null;
  }
}

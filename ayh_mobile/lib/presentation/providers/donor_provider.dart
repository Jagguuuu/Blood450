import 'package:flutter/foundation.dart';
import '../../data/repositories/donor_repository.dart';
import '../../data/models/donor_profile.dart';

class DonorProvider with ChangeNotifier {
  final DonorRepository _repository = DonorRepository();

  DonorProfile? _profile;
  List<DonorProfile> _allDonors = [];
  bool _isLoading = false;
  String? _error;

  DonorProfile? get profile => _profile;
  List<DonorProfile> get allDonors => _allDonors;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadMyProfile() async {
    _isLoading = true;
    notifyListeners();

    try {
      _profile = await _repository.getMyProfile();
      _error = null;
    } catch (e) {
      _error = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<bool> createProfile({
    required String phone,
    required String bloodGroup,
    bool isAvailable = true,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _profile = await _repository.createProfile(
        phone: phone,
        bloodGroup: bloodGroup,
        isAvailable: isAvailable,
      );
      
      _isLoading = false;
      notifyListeners();
      return _profile != null;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> updateProfile({
    String? phone,
    String? bloodGroup,
    bool? isAvailable,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _profile = await _repository.updateMyProfile(
        phone: phone,
        bloodGroup: bloodGroup,
        isAvailable: isAvailable,
      );
      
      _isLoading = false;
      notifyListeners();
      return _profile != null;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> loadAllDonors() async {
    _isLoading = true;
    notifyListeners();

    try {
      _allDonors = await _repository.getAllDonors();
      _error = null;
    } catch (e) {
      _error = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }
}

import 'package:flutter/foundation.dart';
import 'dart:convert';
import '../services/api_service.dart';

class NGO {
  final String name;
  final String contact;
  final String email;
  final String address;
  final List<String> services;
  final String website;

  NGO({
    required this.name,
    required this.contact,
    required this.email,
    required this.address,
    required this.services,
    required this.website,
  });

  factory NGO.fromJson(Map<String, dynamic> json) {
    return NGO(
      name: json['name'] ?? '',
      contact: json['contact'] ?? '',
      email: json['email'] ?? '',
      address: json['address'] ?? '',
      services: List<String>.from(json['services'] ?? []),
      website: json['website'] ?? '',
    );
  }
}

class NGOProvider with ChangeNotifier {
  final ApiService _apiService;
  List<NGO> _ngos = [];
  bool _isLoading = false;
  String? _error;

  NGOProvider({required ApiService apiService}) : _apiService = apiService;

  List<NGO> get ngos => _ngos;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> searchNGOs(String query, {String? category, String? location}) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      String url = '/cases/ngos/search?query=$query';
      if (category != null) url += '&category=$category';
      if (location != null) url += '&location=$location';

      final response = await _apiService.searchNGOs(url);
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        _ngos = data.map((json) => NGO.fromJson(json)).toList();
        _error = null;
      } else {
        _error = 'Failed to search NGOs';
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> getNGOsByCategory(String category, {String? location}) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      String url = '/cases/ngos/category/$category';
      if (location != null) url += '?location=$location';

      final response = await _apiService.getNGOsByCategory(url);
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        _ngos = data.map((json) => NGO.fromJson(json)).toList();
        _error = null;
      } else {
        _error = 'Failed to get NGOs by category';
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> getNGOsByLocation(String location, {String? category}) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      String url = '/cases/ngos/location/$location';
      if (category != null) url += '?category=$category';

      final response = await _apiService.getNGOsByLocation(url);
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        _ngos = data.map((json) => NGO.fromJson(json)).toList();
        _error = null;
      } else {
        _error = 'Failed to get NGOs by location';
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
} 
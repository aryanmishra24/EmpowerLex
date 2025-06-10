import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/user.dart';
import '../models/case.dart';
import '../models/feedback.dart';

class ApiService {
  final String baseUrl;
  final FlutterSecureStorage storage;

  ApiService({
    this.baseUrl = 'http://127.0.0.1:8000', // Updated for local backend
    FlutterSecureStorage? storage,
  }) : storage = storage ?? const FlutterSecureStorage();

  Future<String?> getToken() async => await storage.read(key: 'token');

  Map<String, String> _getHeaders() => {
        'Content-Type': 'application/json',
      };

  Future<Map<String, String>> _getAuthHeaders() async {
    final token = await getToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // Auth endpoints
  Future<http.Response> login(String username, String password) async {
    return await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: _getHeaders(),
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );
  }

  Future<http.Response> signup(Map<String, dynamic> data) async {
    return await http.post(
      Uri.parse('$baseUrl/auth/signup'),
      headers: _getHeaders(),
      body: jsonEncode(data),
    );
  }

  Future<http.Response> getCurrentUser() async {
    return await http.get(
      Uri.parse('$baseUrl/auth/me'),
      headers: await _getAuthHeaders(),
    );
  }

  // Case endpoints
  Future<http.Response> getCases() async {
    print('API: Getting cases...');
    try {
    final response = await http.get(
      Uri.parse('$baseUrl/cases/'),
      headers: await _getAuthHeaders(),
    );
    print('API: Get cases response status: ${response.statusCode}');
    print('API: Get cases response body: ${response.body}');
      
      if (response.statusCode == 401) {
        print('API: Unauthorized - Token may be invalid or expired');
        throw Exception('Unauthorized - Please login again');
      }
      
      if (response.statusCode >= 400) {
        print('API: Error response - ${response.statusCode}: ${response.body}');
        throw Exception('Failed to load cases: ${response.body}');
      }
      
    return response;
    } catch (e) {
      print('API: Error getting cases: $e');
      rethrow;
    }
  }

  Future<http.Response> getCase(String id) async {
    return await _makeRequest('GET', '/cases/$id');
  }

  Future<http.Response> createCase(Map<String, dynamic> data) async {
    print('API: Creating case with data: $data');
    final response = await http.post(
      Uri.parse('$baseUrl/cases/'),
      headers: await _getAuthHeaders(),
      body: jsonEncode(data),
    );
    print('API: Create case response status: ${response.statusCode}');
    print('API: Create case response body: ${response.body}');
    return response;
  }

  // Feedback endpoints
  Future<http.Response> addFeedback(String id, Map<String, dynamic> data) async {
    return await _makeRequest('POST', '/cases/$id/feedback', body: data);
  }

  Future<http.Response> updateCaseStatus(String id, String status) async {
    return await _makeRequest('PATCH', '/cases/$id', body: {'status': status});
  }

  // Next steps endpoints
  Future<http.Response> getNextSteps(String caseId) async {
    return await _makeRequest('GET', '/cases/$caseId/next-steps');
  }

  Future<http.Response> updateNextSteps(String caseId, List<String> steps) async {
    return await _makeRequest('POST', '/cases/$caseId/next-steps', body: {'steps': steps});
  }

  // NGO finder endpoints
  Future<http.Response> searchNGOs(String url) async {
    return await _makeRequest('GET', url);
  }

  Future<http.Response> getNGOsByCategory(String url) async {
    return await _makeRequest('GET', url);
  }

  Future<http.Response> getNGOsByLocation(String url) async {
    return await _makeRequest('GET', url);
  }

  // Helper methods for parsing responses
  User parseUser(Map<String, dynamic> json) => User.fromJson(json);
  Case parseCase(Map<String, dynamic> json) => Case.fromJson(json);

  Future<http.Response> _makeRequest(String method, String path, {Map<String, dynamic>? body}) async {
    // Remove leading slash from path to prevent double slashes
    final cleanPath = path.startsWith('/') ? path.substring(1) : path;
    final uri = Uri.parse('$baseUrl/$cleanPath');
    final headers = await _getAuthHeaders();

    http.Response response;
    if (method == 'GET') {
      response = await http.get(uri, headers: headers);
    } else if (method == 'POST') {
      response = await http.post(
        uri,
        headers: headers,
        body: jsonEncode(body),
      );
    } else if (method == 'PATCH') {
      response = await http.patch(
        uri,
        headers: headers,
        body: jsonEncode(body),
      );
    } else {
      throw Exception('Unsupported HTTP method: $method');
    }

    print('API: ${method.toUpperCase()} ${uri.path} response status: ${response.statusCode}');
    print('API: ${method.toUpperCase()} ${uri.path} response body: ${response.body}');

    // Check for error status codes
    if (response.statusCode >= 400) {
      print('API: Error response - ${response.statusCode}: ${response.body}');
      throw Exception('API request failed with status ${response.statusCode}: ${response.body}');
    }

    return response;
  }
}

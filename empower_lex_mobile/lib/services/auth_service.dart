import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/user.dart';
import 'api_service.dart';

class AuthService {
  final FlutterSecureStorage storage;
  final ApiService apiService;
  static const String tokenKey = 'token';
  static const String userKey = 'user';

  AuthService({required this.apiService, FlutterSecureStorage? storage})
      : storage = storage ?? const FlutterSecureStorage();

  Future<void> saveToken(String token) async {
    await storage.write(key: tokenKey, value: token);
  }

  Future<void> saveUser(User user) async {
    await storage.write(key: userKey, value: jsonEncode(user.toJson()));
  }

  Future<String?> getToken() async {
    return await storage.read(key: tokenKey);
  }

  Future<User?> getUser() async {
    final userJson = await storage.read(key: userKey);
    if (userJson == null) return null;
    return User.fromJson(jsonDecode(userJson));
  }

  Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null;
  }

  Future<void> logout() async {
    await storage.delete(key: tokenKey);
    await storage.delete(key: userKey);
  }

  Future<bool> login(String username, String password) async {
    try {
      final response = await apiService.login(username, password);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await saveToken(data['access_token']);
        
        // Get and save user data
        final userResponse = await apiService.getCurrentUser();
        if (userResponse.statusCode == 200) {
          final userData = jsonDecode(userResponse.body);
          await saveUser(apiService.parseUser(userData));
          return true;
        }
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<bool> signup(Map<String, dynamic> data) async {
    try {
      final response = await apiService.signup(data);
      if (response.statusCode == 200) {
        return await login(data['username'], data['password']);
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}

import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../services/auth_service.dart';

class UserProvider with ChangeNotifier {
  final AuthService authService;
  User? _user;
  bool _isLoading = false;
  String? _error;
  bool _initialLoadDone = false;

  UserProvider({required this.authService}) {
    // Load user data when provider is created
    loadUser();
  }

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isLoggedIn => _user != null;
  bool get initialLoadDone => _initialLoadDone;

  Future<void> loadUser() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final user = await authService.getUser();
      if (user != null) {
        _user = user;
        _error = null;
      } else {
        _error = 'No saved user found';
      }
    } catch (e) {
      _error = e.toString();
      _user = null;
    } finally {
      _isLoading = false;
      _initialLoadDone = true;
      notifyListeners();
    }
  }

  Future<bool> login(String username, String password) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final success = await authService.login(username, password);
      if (success) {
        _initialLoadDone = false; // Reset initial load flag
        await loadUser(); // Reload user data
        return true;
      }
      _error = 'Login failed';
      return false;
    } catch (e) {
      _error = e.toString();
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> signup(Map<String, dynamic> data) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final success = await authService.signup(data);
      if (success) {
        await loadUser();
        return true;
      }
      _error = 'Signup failed';
      return false;
    } catch (e) {
      _error = e.toString();
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    try {
      await authService.logout();
      _user = null;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}

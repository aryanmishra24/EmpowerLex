import 'package:flutter/foundation.dart';
import 'dart:convert';
import '../services/api_service.dart';
import '../models/case.dart';
import '../models/feedback.dart';

class CaseProvider with ChangeNotifier {
  final ApiService _apiService;
  List<Case> _cases = [];
  Case? _currentCase;
  bool _isLoading = false;
  String? _error;
  String _currentFilter = 'all';

  CaseProvider({required ApiService apiService}) : _apiService = apiService;

  List<Case> get cases => _filteredCases;
  Case? get currentCase => _currentCase;
  bool get isLoading => _isLoading;
  String? get error => _error;
  String get currentFilter => _currentFilter;

  List<Case> get _filteredCases {
    if (_currentFilter == 'all') return _cases;
    return _cases.where((case_) => case_.status == _currentFilter).toList();
  }

  void setFilter(String filter) {
    _currentFilter = filter;
    notifyListeners();
  }

  Future<void> loadCases() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      print('CaseProvider: Loading cases...');
      final response = await _apiService.getCases();
      print('CaseProvider: Response received with status ${response.statusCode}');
      
      if (response.statusCode != 200) {
        _error = 'Server error: ${response.statusCode}';
        print('CaseProvider: Error - $_error');
        return;
      }

      final List<dynamic> data = jsonDecode(response.body);
      print('CaseProvider: Parsed ${data.length} cases from response');
      
      _cases = [];
      for (var json in data) {
        try {
          print('CaseProvider: Parsing case: ${json['title']}');
          print('CaseProvider: Case data: $json');
          
          // Ensure required fields are present
          if (!json.containsKey('case_id') || !json.containsKey('title')) {
            print('CaseProvider: Skipping case with missing required fields');
            continue;
          }
          
          final case_ = Case.fromJson(json);
          _cases.add(case_);
          print('CaseProvider: Successfully parsed case: ${case_.title}');
        } catch (e, stackTrace) {
          print('CaseProvider: Error parsing case: $e');
          print('CaseProvider: Stack trace: $stackTrace');
          print('CaseProvider: Problematic JSON: $json');
          // Don't rethrow, continue with other cases
        }
      }
      
      print('CaseProvider: Successfully loaded ${_cases.length} cases');
      if (_cases.isNotEmpty) {
        print('CaseProvider: First case title: ${_cases.first.title}');
      } else {
        print('CaseProvider: No cases found');
      }
      _error = null;
    } catch (e, stackTrace) {
      _error = e.toString();
      print('CaseProvider: Error loading cases: $_error');
      print('CaseProvider: Stack trace: $stackTrace');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadCase(String id) async {
    try {
      _isLoading = true;
      notifyListeners();
      final response = await _apiService.getCase(id);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _currentCase = Case.fromJson(data);
        _error = null;
      } else {
        _error = 'Failed to load case';
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> createCase(Map<String, dynamic> caseData) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.createCase(caseData);
      if (response.statusCode == 200 || response.statusCode == 201) {
        await loadCases();
        return true;
      }
      _error = 'Failed to create case';
      return false;
    } catch (e) {
      _error = e.toString();
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> addFeedback(String caseId, String feedback, int rating) async {
    try {
      _isLoading = true;
      notifyListeners();
      
      final response = await _apiService.addFeedback(caseId, {
        'case_id': caseId,
        'comments': feedback,
        'rating': rating,
      });
      
      if (response.statusCode == 200) {
        await loadCase(caseId);  // Reload the case to get updated feedback
        _error = null;
        return true;
      }
      
      _error = 'Failed to add feedback';
      return false;
    } catch (e) {
      _error = e.toString();
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> updateCaseStatus(String id, String status) async {
    try {
      _isLoading = true;
      notifyListeners();
      final response = await _apiService.updateCaseStatus(id, status);
      if (response.statusCode == 200) {
        await Future.wait([
          loadCase(id),
          loadCases()
        ]);
        _error = null;
      } else {
        _error = 'Failed to update case status';
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Next steps methods
  Future<List<String>> getNextSteps(String caseId) async {
    try {
      _isLoading = true;
      notifyListeners();
      final response = await _apiService.getNextSteps(caseId);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<String>.from(data['steps']);
      }
      _error = 'Failed to load next steps';
      return [];
    } catch (e) {
      _error = e.toString();
      return [];
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> updateNextSteps(String caseId, List<String> steps) async {
    try {
      _isLoading = true;
      notifyListeners();
      final response = await _apiService.updateNextSteps(caseId, steps);
      if (response.statusCode == 200) {
        await loadCase(caseId);
        _error = null;
        return true;
      }
      _error = 'Failed to update next steps';
      return false;
    } catch (e) {
      _error = e.toString();
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}

import 'feedback.dart';

class Case {
  final String id;
  final String title;
  final String description;
  final String category;
  final String priority;
  final String status;
  final String generatedDraft;
  final List<Map<String, dynamic>> applicableLaws;
  final List<Map<String, dynamic>> suggestedNGOs;
  final List<String> nextSteps;
  final List<CaseFeedback> feedback;
  final DateTime createdAt;
  final DateTime? updatedAt;

  Case({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required this.priority,
    required this.status,
    required this.generatedDraft,
    required this.applicableLaws,
    required this.suggestedNGOs,
    required this.nextSteps,
    required this.feedback,
    required this.createdAt,
    this.updatedAt,
  });

  factory Case.fromJson(Map<String, dynamic> json) {
    return Case(
      id: json['case_id'] ?? '',
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      category: json['category'] ?? '',
      priority: json['priority'] ?? '',
      status: json['status'] ?? '',
      generatedDraft: json['generated_draft'] ?? '',
      applicableLaws: (json['applicable_laws'] as List<dynamic>?)?.map((law) => 
        Map<String, dynamic>.from(law as Map)).toList() ?? [],
      suggestedNGOs: (json['suggested_ngos'] as List<dynamic>?)?.map((ngo) => 
        Map<String, dynamic>.from(ngo as Map)).toList() ?? [],
      nextSteps: (json['next_steps'] as List<dynamic>?)?.map((step) => 
        step.toString()).toList() ?? [],
      feedback: (json['feedback'] as List<dynamic>?)?.map((f) => 
        CaseFeedback.fromJson(f as Map<String, dynamic>)).toList() ?? [],
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'case_id': id,
      'title': title,
      'description': description,
      'category': category,
      'status': status,
      'priority': priority,
      'generated_draft': generatedDraft,
      'applicable_laws': applicableLaws,
      'suggested_ngos': suggestedNGOs,
      'next_steps': nextSteps,
      'feedback': feedback.map((f) => f.toJson()).toList(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}

class CaseFeedback {
  final int id;
  final String content;
  final int? rating;
  final String userName;
  final DateTime createdAt;

  CaseFeedback({
    required this.id,
    required this.content,
    this.rating,
    required this.userName,
    required this.createdAt,
  });

  factory CaseFeedback.fromJson(Map<String, dynamic> json) {
    return CaseFeedback(
      id: json['id'] ?? 0,
      content: json['comments'] ?? '',  // Note: backend uses 'comments' field
      rating: json['rating'],
      userName: json['user_name'] ?? 'Anonymous',
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'comments': content,
      'rating': rating,
      'user_name': userName,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

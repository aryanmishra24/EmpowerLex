import 'package:share_plus/share_plus.dart';

class DocumentService {
  static Future<void> generateLegalDraft({
    required String title,
    required String category,
    required String status,
    required String draft,
  }) async {
    try {
      // Create the document content
      final content = '''
LEGAL DRAFT
===========

Title: $title
Category: $category
Status: $status
Date: ${DateTime.now().toString().split(' ')[0]}

Draft Content:
-------------
$draft
''';

      // Share the content directly
      await Share.share(
        content,
        subject: 'Legal Draft: $title',
      );
    } catch (e) {
      print('Error sharing document: $e');
      rethrow;
    }
  }
} 
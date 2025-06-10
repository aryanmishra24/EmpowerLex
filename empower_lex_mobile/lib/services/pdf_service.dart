import 'dart:io';
import 'package:flutter/services.dart';
import 'package:docx_template/docx_template.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

class DocumentService {
  static Future<void> generateLegalDraft({
    required String title,
    required String category,
    required String status,
    required String draft,
  }) async {
    try {
      // Load the template
      final templateBytes = await rootBundle.load('assets/templates/legal_draft_template.txt');
      final template = DocxTemplate.fromBytes(templateBytes.buffer.asUint8List());

      // Prepare the data
      final data = {
        'title': title,
        'category': category,
        'status': status,
        'date': DateTime.now().toString().split(' ')[0],
        'draft': draft,
      };

      // Generate the document
      final doc = await template.generate(data);

      // Save to temporary directory
      final tempDir = await getTemporaryDirectory();
      final file = File('${tempDir.path}/$title.docx');
      await file.writeAsBytes(doc);

      // Share the document
      await Share.shareXFiles([XFile(file.path)], text: 'Legal Draft: $title');
    } catch (e) {
      print('Error generating document: $e');
      rethrow;
    }
  }
} 
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/case_provider.dart';
import '../models/case.dart';
import '../widgets/feedback_card.dart';
import '../services/document_service.dart';
import 'feedback_screen.dart';
import 'next_steps_screen.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

class CaseDetailScreen extends StatefulWidget {
  final String id;

  const CaseDetailScreen({
    Key? key,
    required this.id,
  }) : super(key: key);

  @override
  State<CaseDetailScreen> createState() => _CaseDetailScreenState();
}

class _CaseDetailScreenState extends State<CaseDetailScreen> {
  // Helper to extract main draft and legal analysis
  Map<String, String> extractDraftAndAnalysis(String draft) {
    try {
      final analysisMap = json.decode(draft);
      if (analysisMap is Map && analysisMap.containsKey('analysis')) {
        String analysis = analysisMap['analysis'].replaceAll(r'\n', '\n');
        // If you have a separate draft content, extract it here. Otherwise, show nothing or a placeholder.
        return {
          'draft': '', // or analysisMap['draft'] if available
          'analysis': analysis,
        };
      }
    } catch (_) {}
    // Fallback: treat the whole thing as draft, no separate analysis
    return {
      'draft': draft.replaceAll(r'\n', '\n'),
      'analysis': '',
    };
  }

  @override
  void initState() {
    super.initState();
    print('CaseDetailScreen: initState called for case  ${widget.id}');
    Future.microtask(() {
      print('CaseDetailScreen: Loading case ${widget.id}');
      context.read<CaseProvider>().loadCase(widget.id);
    });
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'pending':
        return Colors.orange;
      case 'in_progress':
        return Colors.blue;
      case 'completed':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      case 'low':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.grey[700],
              ),
            ),
          ),
          Expanded(
            child: Text(value),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    print('CaseDetailScreen: Building...');
    return Scaffold(
      appBar: AppBar(
        title: const Text('Case Details'),
        actions: [
          IconButton(
            icon: const Icon(Icons.description),
            onPressed: () async {
              final caseProvider = Provider.of<CaseProvider>(context, listen: false);
              final caseData = caseProvider.currentCase;
              if (caseData != null) {
                try {
                  await DocumentService.generateLegalDraft(
                    title: caseData.title,
                    category: caseData.category,
                    status: caseData.status,
                    draft: caseData.generatedDraft,
                  );
                } catch (e) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Error generating document: $e')),
                  );
                }
              }
            },
          ),
        ],
      ),
      body: Consumer<CaseProvider>(
        builder: (context, caseProvider, child) {
          print('CaseDetailScreen: Consumer rebuilding');
          print('CaseDetailScreen: isLoading=${caseProvider.isLoading}');
          print('CaseDetailScreen: error=${caseProvider.error}');
          print('CaseDetailScreen: currentCase=${caseProvider.currentCase?.title}');

          if (caseProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (caseProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Error: ${caseProvider.error}',
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      print('CaseDetailScreen: Retrying load case ${widget.id}');
                      caseProvider.loadCase(widget.id);
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          final case_ = caseProvider.currentCase;
          if (case_ == null) {
            print('CaseDetailScreen: Case not found');
            return const Center(child: Text('Case not found'));
          }

          print('CaseDetailScreen: Building case details for ${case_.title}');
          return Scaffold(
            backgroundColor: Colors.grey[100],
            body: SafeArea(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Title Section
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      color: Colors.white,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            case_.title,
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 8),
                          Row(
                            children: [
                              Container(
                                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: _getStatusColor(case_.status),
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                child: DropdownButton<String>(
                                  value: case_.status,
                                  dropdownColor: _getStatusColor(case_.status),
                                  underline: SizedBox(),
                                  icon: Icon(Icons.arrow_drop_down, color: Colors.white),
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                  items: ['pending', 'in_progress', 'completed']
                                      .map((String status) {
                                    return DropdownMenuItem<String>(
                                      value: status,
                                      child: Text(status.toUpperCase()),
                                    );
                                  }).toList(),
                                  onChanged: (String? newStatus) async {
                                    if (newStatus != null && newStatus != case_.status) {
                                      try {
                                        await caseProvider.updateCaseStatus(widget.id, newStatus);
                                        ScaffoldMessenger.of(context).showSnackBar(
                                          SnackBar(
                                            content: Text('Status updated successfully'),
                                            backgroundColor: Colors.green,
                                          ),
                                        );
                                      } catch (e) {
                                        ScaffoldMessenger.of(context).showSnackBar(
                                          SnackBar(
                                            content: Text('Failed to update status: $e'),
                                            backgroundColor: Colors.red,
                                          ),
                                        );
                                      }
                                    }
                                  },
                                ),
                              ),
                              SizedBox(width: 8),
                              Container(
                                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: _getPriorityColor(case_.priority),
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                child: Text(
                                  case_.priority.toUpperCase(),
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 16),
                    // Description Section
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      color: Colors.white,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Description',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 8),
                          MarkdownBody(data: case_.description),
                        ],
                      ),
                    ),
                    SizedBox(height: 16),
                    // Draft Section
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      color: Colors.white,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Legal Draft',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              ElevatedButton.icon(
                                onPressed: () async {
                                  try {
                                    await DocumentService.generateLegalDraft(
                                      title: case_.title,
                                      category: case_.category,
                                      status: case_.status,
                                      draft: case_.generatedDraft,
                                    );
                                  } catch (e) {
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      SnackBar(
                                        content: Text('Failed to generate document: $e'),
                                        backgroundColor: Colors.red,
                                      ),
                                    );
                                  }
                                },
                                icon: Icon(Icons.download),
                                label: Text('Download Document'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Theme.of(context).primaryColor,
                                  foregroundColor: Colors.white,
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 8),
                          if (case_.generatedDraft.isNotEmpty) ...[
                            Builder(
                              builder: (context) {
                                final draftAndAnalysis = extractDraftAndAnalysis(case_.generatedDraft);
                                final draftContent = draftAndAnalysis['draft'] ?? '';
                                final analysis = draftAndAnalysis['analysis'] ?? '';
                                return Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    if (draftContent.isNotEmpty)
                                      MarkdownBody(data: draftContent),
                                    if (analysis.isNotEmpty) ...[
                                      SizedBox(height: 16),
                                      Text('LEGAL ANALYSIS:', style: TextStyle(fontWeight: FontWeight.bold)),
                                      MarkdownBody(data: analysis),
                                    ],
                                  ],
                                );
                              },
                            ),
                          ],
                        ],
                      ),
                    ),
                    SizedBox(height: 16),
                    // Next Steps Section
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      color: Colors.white,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Next Steps',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              ElevatedButton.icon(
                                onPressed: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => NextStepsScreen(caseId: widget.id),
                                    ),
                                  );
                                },
                                icon: Icon(Icons.add_task),
                                label: Text('Manage'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Theme.of(context).primaryColor,
                                  foregroundColor: Colors.white,
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 8),
                          if (case_.nextSteps.isEmpty)
                            Text(
                              'No next steps added yet',
                              style: TextStyle(
                                color: Colors.grey[600],
                                fontStyle: FontStyle.italic,
                              ),
                            )
                          else
                            ListView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              itemCount: case_.nextSteps.length,
                              itemBuilder: (context, index) {
                                return ListTile(
                                  leading: CircleAvatar(
                                    child: Text('${index + 1}'),
                                  ),
                                  title: MarkdownBody(data: case_.nextSteps[index]),
                                );
                              },
                            ),
                        ],
                      ),
                    ),
                    SizedBox(height: 16),
                    // Feedback Section
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      color: Colors.white,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Feedback',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              ElevatedButton.icon(
                                onPressed: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => FeedbackScreen(caseId: widget.id),
                                    ),
                                  );
                                },
                                icon: Icon(Icons.feedback),
                                label: Text('Add'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Theme.of(context).primaryColor,
                                  foregroundColor: Colors.white,
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 8),
                          if (case_.feedback.isEmpty)
                            Text(
                              'No feedback yet',
                              style: TextStyle(
                                color: Colors.grey[600],
                                fontStyle: FontStyle.italic,
                              ),
                            )
                          else
                            ListView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              itemCount: case_.feedback.length,
                              itemBuilder: (context, index) {
                                return FeedbackCard(feedback: case_.feedback[index]);
                              },
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

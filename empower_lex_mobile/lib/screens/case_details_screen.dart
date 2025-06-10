import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:empower_lex_mobile/providers/case_provider.dart';
import 'package:empower_lex_mobile/screens/next_steps_screen.dart';

class CaseDetailsScreen extends StatefulWidget {
  final String caseId;

  const CaseDetailsScreen({Key? key, required this.caseId}) : super(key: key);

  @override
  _CaseDetailsScreenState createState() => _CaseDetailsScreenState();
}

class _CaseDetailsScreenState extends State<CaseDetailsScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Case Details'),
        actions: [
          IconButton(
            icon: Icon(Icons.list),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => NextStepsScreen(caseId: widget.caseId),
                ),
              );
            },
          ),
        ],
      ),
      body: Consumer<CaseProvider>(
        builder: (context, caseProvider, child) {
          if (caseProvider.isLoading) {
            return Center(child: CircularProgressIndicator());
          }

          final case_ = caseProvider.currentCase;
          if (case_ == null) {
            return Center(child: Text('Case not found'));
          }

          return SingleChildScrollView(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  case_.title,
                  style: Theme.of(context).textTheme.headline5,
                ),
                SizedBox(height: 8),
                Text('Status: ${case_.status}'),
                SizedBox(height: 16),
                Text(
                  'Description',
                  style: Theme.of(context).textTheme.headline6,
                ),
                Text(case_.description),
                SizedBox(height: 16),
                Text(
                  'Next Steps',
                  style: Theme.of(context).textTheme.headline6,
                ),
                ElevatedButton.icon(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => NextStepsScreen(caseId: widget.caseId),
                      ),
                    );
                  },
                  icon: Icon(Icons.add_task),
                  label: Text('Manage Next Steps'),
                ),
                SizedBox(height: 16),
                Text(
                  'Feedback',
                  style: Theme.of(context).textTheme.headline6,
                ),
                // ... rest of the existing code ...
              ],
            ),
          );
        },
      ),
    );
  }
} 
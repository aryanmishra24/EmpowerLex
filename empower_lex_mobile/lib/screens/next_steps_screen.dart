import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../providers/case_provider.dart';

class NextStepsScreen extends StatefulWidget {
  final String caseId;

  const NextStepsScreen({Key? key, required this.caseId}) : super(key: key);

  @override
  _NextStepsScreenState createState() => _NextStepsScreenState();
}

class _NextStepsScreenState extends State<NextStepsScreen> {
  final TextEditingController _stepController = TextEditingController();
  List<String> _steps = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadSteps();
  }

  Future<void> _loadSteps() async {
    setState(() => _isLoading = true);
    final caseProvider = Provider.of<CaseProvider>(context, listen: false);
    final steps = await caseProvider.getNextSteps(widget.caseId);
    setState(() {
      _steps = steps;
      _isLoading = false;
    });
  }

  Future<void> _addStep() async {
    if (_stepController.text.isEmpty) return;

    setState(() => _isLoading = true);
    final caseProvider = Provider.of<CaseProvider>(context, listen: false);
    final updatedSteps = List<String>.from(_steps)..add(_stepController.text);
    
    final success = await caseProvider.updateNextSteps(widget.caseId, updatedSteps);
    if (success) {
      setState(() {
        _steps = updatedSteps;
        _stepController.clear();
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to add step')),
      );
    }
    setState(() => _isLoading = false);
  }

  Future<void> _removeStep(int index) async {
    setState(() => _isLoading = true);
    final caseProvider = Provider.of<CaseProvider>(context, listen: false);
    final updatedSteps = List<String>.from(_steps)..removeAt(index);
    
    final success = await caseProvider.updateNextSteps(widget.caseId, updatedSteps);
    if (success) {
      setState(() => _steps = updatedSteps);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to remove step')),
      );
    }
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Next Steps'),
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _stepController,
                          decoration: InputDecoration(
                            hintText: 'Enter next step',
                            border: OutlineInputBorder(),
                          ),
                        ),
                      ),
                      SizedBox(width: 16),
                      ElevatedButton(
                        onPressed: _addStep,
                        child: Text('Add'),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: _steps.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        leading: CircleAvatar(
                          child: Text('${index + 1}'),
                        ),
                        title: MarkdownBody(data: _steps[index]),
                        trailing: IconButton(
                          icon: Icon(Icons.delete),
                          onPressed: () => _removeStep(index),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
    );
  }

  @override
  void dispose() {
    _stepController.dispose();
    super.dispose();
  }
} 
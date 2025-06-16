import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/user_provider.dart';
import '../providers/case_provider.dart';
import '../widgets/case_card.dart';
import 'create_case_screen.dart';
import 'case_detail_screen.dart';
import 'ngo_finder_screen.dart';
import 'case_filter.dart';
import 'login_screen.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    print('DashboardScreen: initState called');
    Future.microtask(() {
      print('DashboardScreen: Loading cases...');
      context.read<CaseProvider>().loadCases();
    });
  }

  @override
  Widget build(BuildContext context) {
    print('DashboardScreen: Building...');
    return Scaffold(
      appBar: AppBar(
        title: Text('My Cases'),
        actions: [
          IconButton(
            icon: Icon(Icons.search),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => NGOFinderScreen()),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () async {
              final created = await Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => CreateCaseScreen()),
              );
              if (created == true) {
                context.read<CaseProvider>().loadCases();
              }
            },
          ),
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () async {
              await context.read<UserProvider>().logout();
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (_) => LoginScreen()),
                (route) => false,
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

          if (caseProvider.error != null) {
            return Center(
              child: Text('Error: ${caseProvider.error}'),
            );
          }

          final cases = caseProvider.cases;

          if (cases.isEmpty) {
            return Column(
              children: [
                CaseFilter(
                  selectedFilter: caseProvider.currentFilter,
                  onFilterChanged: (filter) => caseProvider.setFilter(filter),
                ),
                Expanded(
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'No cases found for this filter',
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => CreateCaseScreen()),
                            );
                          },
                          child: Text('Create New Case'),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            );
          }

          return Column(
            children: [
              CaseFilter(
                selectedFilter: caseProvider.currentFilter,
                onFilterChanged: (filter) => caseProvider.setFilter(filter),
              ),
              Expanded(
                child: ListView.builder(
                  itemCount: cases.length,
                  itemBuilder: (context, index) {
                    final case_ = cases[index];
                    return CaseCard(
                      case_: case_,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => CaseDetailScreen(id: case_.id),
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

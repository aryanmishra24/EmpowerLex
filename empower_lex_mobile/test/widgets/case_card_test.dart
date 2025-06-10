import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../../lib/widgets/case_card.dart';
import '../../lib/models/case.dart';

void main() {
  testWidgets('CaseCard displays case information correctly',
      (WidgetTester tester) async {
    final case_ = Case(
      id: 1,
      title: 'Test Case',
      description: 'Test Description',
      category: 'Legal',
      priority: 'High',
      status: 'pending',
      createdAt: DateTime(2024, 1, 1),
      updatedAt: null,
      feedback: [],
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: CaseCard(
            case_: case_,
            onTap: () {},
          ),
        ),
      ),
    );

    expect(find.text('Test Case'), findsOneWidget);
    expect(find.text('Test Description'), findsOneWidget);
    expect(find.text('Legal'), findsOneWidget);
    expect(find.text('High'), findsOneWidget);
    expect(find.text('PENDING'), findsOneWidget);
    expect(find.text('1/1/2024'), findsOneWidget);
  });

  testWidgets('CaseCard handles different status colors',
      (WidgetTester tester) async {
    final cases = [
      Case(
        id: 1,
        title: 'Pending Case',
        description: 'Description',
        category: 'Legal',
        priority: 'High',
        status: 'pending',
        createdAt: DateTime(2024, 1, 1),
        updatedAt: null,
        feedback: [],
      ),
      Case(
        id: 2,
        title: 'In Progress Case',
        description: 'Description',
        category: 'Legal',
        priority: 'High',
        status: 'in_progress',
        createdAt: DateTime(2024, 1, 1),
        updatedAt: null,
        feedback: [],
      ),
      Case(
        id: 3,
        title: 'Completed Case',
        description: 'Description',
        category: 'Legal',
        priority: 'High',
        status: 'completed',
        createdAt: DateTime(2024, 1, 1),
        updatedAt: null,
        feedback: [],
      ),
    ];

    for (final case_ in cases) {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CaseCard(
              case_: case_,
              onTap: () {},
            ),
          ),
        ),
      );

      final statusChip = tester.widget<Chip>(
        find.ancestor(
          of: find.text(case_.status.toUpperCase()),
          matching: find.byType(Chip),
        ),
      );

      Color expectedColor;
      switch (case_.status.toLowerCase()) {
        case 'pending':
          expectedColor = Colors.orange;
          break;
        case 'in_progress':
          expectedColor = Colors.blue;
          break;
        case 'completed':
          expectedColor = Colors.green;
          break;
        default:
          expectedColor = Colors.grey;
      }

      expect(statusChip.backgroundColor, expectedColor);
    }
  });

  testWidgets('CaseCard calls onTap when tapped', (WidgetTester tester) async {
    bool tapped = false;
    final case_ = Case(
      id: 1,
      title: 'Test Case',
      description: 'Test Description',
      category: 'Legal',
      priority: 'High',
      status: 'pending',
      createdAt: DateTime(2024, 1, 1),
      updatedAt: null,
      feedback: [],
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: CaseCard(
            case_: case_,
            onTap: () => tapped = true,
          ),
        ),
      ),
    );

    await tester.tap(find.byType(CaseCard));
    await tester.pump();

    expect(tapped, isTrue);
  });
} 
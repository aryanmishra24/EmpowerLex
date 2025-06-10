import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../../lib/widgets/feedback_card.dart';
import '../../lib/models/feedback.dart';

void main() {
  testWidgets('FeedbackCard displays feedback information correctly',
      (WidgetTester tester) async {
    final feedback = CaseFeedback(
      id: 1,
      content: 'Test Feedback',
      rating: 5,
      userName: 'Test User',
      createdAt: DateTime(2024, 1, 1),
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: FeedbackCard(feedback: feedback),
        ),
      ),
    );

    expect(find.text('Test Feedback'), findsOneWidget);
    expect(find.text('Test User'), findsOneWidget);
    expect(find.text('2024-01-01'), findsOneWidget);
    expect(find.text('5'), findsOneWidget);
    expect(find.byIcon(Icons.star), findsOneWidget);
  });

  testWidgets('FeedbackCard handles feedback without rating',
      (WidgetTester tester) async {
    final feedback = CaseFeedback(
      id: 1,
      content: 'Test Feedback',
      rating: null,
      userName: 'Test User',
      createdAt: DateTime(2024, 1, 1),
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: FeedbackCard(feedback: feedback),
        ),
      ),
    );

    expect(find.text('Test Feedback'), findsOneWidget);
    expect(find.text('Test User'), findsOneWidget);
    expect(find.text('2024-01-01'), findsOneWidget);
    expect(find.byIcon(Icons.star), findsNothing);
  });

  testWidgets('FeedbackCard displays user initial in avatar',
      (WidgetTester tester) async {
    final feedback = CaseFeedback(
      id: 1,
      content: 'Test Feedback',
      rating: 5,
      userName: 'Test User',
      createdAt: DateTime(2024, 1, 1),
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: FeedbackCard(feedback: feedback),
        ),
      ),
    );

    final avatar = tester.widget<CircleAvatar>(
      find.byType(CircleAvatar),
    );

    expect(
      (avatar.child as Text).data,
      'T',
    );
  });
} 
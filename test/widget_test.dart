import 'package:flutter_test/flutter_test.dart';
import 'package:opencode_mobile/main.dart';

void main() {
  testWidgets('Chat screen renders', (WidgetTester tester) async {
    await tester.pumpWidget(const OpenCodeMobileApp());
    expect(find.text('OpenCode Mobile'), findsOneWidget);
    expect(find.text('Envía un mensaje para empezar'), findsOneWidget);
  });
}

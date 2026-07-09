enum MessageRole { user, bot }

class Message {
  final String text;
  final MessageRole role;
  final DateTime timestamp;

  Message({
    required this.text,
    required this.role,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}

from src.jobs.dart_model_to_dto import extract_classes_and_properties


def somestuff():
    dart_content = '''
class ChatSessionModel extends Equatable {
  ChatSessionModel({
    required this.id,
    required this.userId,
    required this.agentId,
    required this.startTime,
    required this.endTime,
    required this.messages,
    required this.projectId,
  });

  final String? id;
  final String? userId;
  final String? agentId;
  final String? startTime;
  final String? endTime;
  final List<ChatMessage>? messages;
  final String? projectId;

  @override
  List<Object?> get props => [
        id,
        userId,
        agentId,
        startTime,
        endTime,
        messages,
        projectId,
      ];

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'agentId': agentId,
      'startTime': startTime,
      'endTime': endTime,
      'messages': messages?.map((e) => e.toJson()).toList(),
      'projectId': projectId,
    };
  }

  factory ChatSessionModel.fromJson(Map<String, dynamic> map) {
    return ChatSessionModel(
      id: map['id'],
      userId: map['userId'],
      agentId: map['agentId'],
      startTime: map['startTime'],
      endTime: map['endTime'],
      messages: parseList<ChatMessage>(
        json: map['messages'],
        fromJson: (a) => ChatMessage.fromJson(a),
      ),
      projectId: map['projectId'],
    );
  }

  ChatSessionModel copyWith(
      {String? id,
      String? userId,
      String? agentId,
      String? startTime,
      String? endTime,
      List<ChatMessage>? messages,
      String? projectId}) {
    return ChatSessionModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      agentId: agentId ?? this.agentId,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
      messages: messages ?? this.messages,
      projectId: projectId ?? this.projectId,
    );
  }

  static Map<String, dynamic> exampleJson() {
    return {
      'id': "",
      'userId': "",
      'agentId': "",
      'startTime': "",
      'endTime': "",
      'messages': [
        ChatMessage.exampleJson(),
      ],
      'projectId': ""
    };
  }

  bool match(Map map) {
    final model = toJson();
    final keys = model.keys.toList();

    for (final query in map.entries) {
      try {
        final trueValue = model[query.key];
        final exists = trueValue == query.value;
        if (exists) {
          return true;
        }
      } catch (e) {
        return false;
      }
    }
    return false;
  }

  static ChatSessionModel example() =>
      ChatSessionModel.fromJson(ChatSessionModel.exampleJson());
}

class ChatMessage extends Equatable {
  ChatMessage(
      {required this.id,
      required this.text,
      required this.sender,
      required this.sessionId,
      required this.timestamp});

  final String? id;
  final String? text;
  final String? sender;
  final String? sessionId;
  final String? timestamp;

  @override
  List<Object?> get props => [id, text, sender, sessionId, timestamp];

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'text': text,
      'sender': sender,
      'sessionId': sessionId,
      'timestamp': timestamp
    };
  }

  factory ChatMessage.fromJson(Map<String, dynamic> map) {
    return ChatMessage(
        id: map['id'],
        text: map['text'],
        sender: map['sender'],
        sessionId: map['sessionId'],
        timestamp: map['timestamp']);
  }

  ChatMessage copyWith(
      {String? id,
      String? text,
      String? sender,
      String? senderId,
      String? sessionId,
      String? timestamp}) {
    return ChatMessage(
        id: id ?? this.id,
        text: text ?? this.text,
        sender: sender ?? this.sender,
        sessionId: sessionId ?? this.sessionId,
        timestamp: timestamp ?? this.timestamp);
  }

  static Map<String, dynamic> exampleJson() {
    return {
      'id': "",
      'text': "",
      'sender': "",
      'senderId': "",
      'sessionId': "",
      'timestamp': ""
    };
  }

  bool match(Map map) {
    final model = toJson();
    final keys = model.keys.toList();

    for (final query in map.entries) {
      try {
        final trueValue = model[query.key];
        final exists = trueValue == query.value;
        if (exists) {
          return true;
        }
      } catch (e) {
        return false;
      }
    }
    return false;
  }

  static ChatMessage example() =>
      ChatMessage.fromJson(ChatMessage.exampleJson());
}

    '''

    classes_and_properties = extract_classes_and_properties(dart_content)
    print(
        classes_and_properties)  # Expected: {'Parent': [('String', 'name'), ('int', 'age')], 'Child': [('String', 'school')]}


somestuff()

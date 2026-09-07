import 'package:flutter/material.dart';

void main() {
  runApp(const TelegramApp());
}

class TelegramApp extends StatelessWidget {
  const TelegramApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Telegram Pro',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0E1621), // لون خلفية تليجرام الداكن الاصلية
      ),
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  // قائمة الرسائل المخزنة حياً في الذاكرة لتحديث الشاشة فوراً
  final List<Map<String, String>> _messages = [
    {"sender": "Waseem", "content": "أهلاً بك في عالم Flutter الخارق! واجهة تليجرام أصبحت أصلية 100% الآن 🔥", "time": "03:15 ص", "isMe": "true"},
    {"sender": "أبو أحمد", "content": "ما شاء الله! الواجهة انسيابية جداً والفقاعات ثابتة وسريعة.", "time": "03:16 ص", "isMe": "false"}
  ];

  final TextEditingController _textController = TextEditingController();

  // دالة إرسال الرسالة الفورية
  void _sendMessage() {
    if (_textController.text.trim().isNotEmpty) {
      setState(() {
        _messages.add({
          "sender": "Waseem",
          "content": _textController.text,
          "time": "04:00 ص",
          "isMe": "true"
        });
      });
      _textController.clear(); // تصفير الحقل فوراً لمنع التكرار نهائياً
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 1. هيدر تليجرام العلوي الأصلي الثابت
      appBar: AppBar(
        backgroundColor: const Color(0xFF17212B),
        elevation: 1,
        title: Directionality(
          textDirection: TextDirection.rtl,
          child: Row(
            children: [
              const CircleAvatar(
                backgroundColor: Color(0xFF2B5278),
                child: Text('🍉', style: TextStyle(fontSize: 20)),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('تلجرام غزة المطور', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  Text('متصل الآن • مدعوم بـ Flutter', style: TextStyle(fontSize: 12, color: const Color(0xFF5288C1))),
                ],
              ),
            ],
          ),
        ),
        actions: [
          IconButton(onPressed: () {}, icon: const Icon(Icons.more_vert, color: Colors.grey)),
        ],
      ),
      
      // 2. ساحة المحادثة وشريط الإدخال السفلي
      body: Column(
        children: [
          // ساحة الرسائل القابلة للتمرير بسلاسة هائلة
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final isMe = msg["isMe"] == "true";

                return Align(
                  alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    decoration: BoxDecoration(
                      color: isMe ? const Color(0xFF2B5278) : const Color(0xFF182533), // ألوان تليجرام للفقاعات
                      borderRadius: BorderRadius.only(
                        topLeft: const Radius.circular(14),
                        topRight: const Radius.circular(14),
                        bottomLeft: isMe ? const Radius.circular(14) : const Radius.circular(4),
                        bottomRight: isMe ? const Radius.circular(4) : const Radius.circular(14),
                      ),
                      boxShadow: [
                        BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 2, offset: const Offset(0, 1))
                      ]
                    ),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        if (!isMe)
                          Text(msg["sender"]!, style: const TextStyle(color: Color(0xFF5288C1), fontSize: 12, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 4),
                        Text(msg["content"]!, style: const TextStyle(color: Colors.white, fontSize: 15)),
                        const SizedBox(height: 4),
                        Row(
                          mainAxisSize: MainAxisSize.min,
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            Text(msg["time"]!, style: TextStyle(color: isMe ? const Color(0xFFABC6E0) : Colors.grey, fontSize: 10)),
                            if (isMe) ...[
                              const SizedBox(width: 4),
                              const Icon(Icons.done_all, color: Color(0xFFABC6E0), size: 14), // علامتين الصح الزرقاء
                            ]
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),

          // 3. صندوق الإدخال السفلي الدائري المطابق لتليجرام والمثبت على الهاتف
          Container(
            color: const Color(0xFF17212B),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              children: [
                IconButton(onPressed: () {}, icon: const Icon(Icons.attach_file, color: Colors.grey)),
                Expanded(
                  child: Directionality(
                    textDirection: TextDirection.rtl,
                    child: TextField(
                      controller: _textController,
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: 'اكتب رسالة...',
                        hintStyle: const TextStyle(color: Colors.grey),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        fillColor: const Color(0xFF0E1621),
                        filled: true,
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                // زر الإرسال الدائري الأزرق
                GestureDetector(
                  onTap: _sendMessage,
                  child: Container(
                    width: 44,
                    height: 44,
                    decoration: const BoxDecoration(
                      color: Color(0xFF2481CC),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.send, color: Colors.white, size: 20),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

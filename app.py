import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# الصفحة الرئيسية (المنيو الذكي)
@app.route('/')
def index():
    # هنا بنقول للسيرفر يفتح ملف index.html اللي بره في الفولدر الرئيسي
    return render_template('index.html')

# الـ Voice AI (لمسة الجدة للرد الصوتي)
@app.route('/voice', methods=['POST'])
def voice():
    user_text = request.json.get("text")
    # هنا مستقبلاً هنربط بـ Gemini بس حالياً بنرجعه عشان الصوت يشتغل
    return jsonify({"reply": f"أبشر، طلبت {user_text}.. تأمرني بشيء ثاني؟"})

if __name__ == "__main__":
    # تشغيل السيرفر على بورت 10000 اللي طالبه Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

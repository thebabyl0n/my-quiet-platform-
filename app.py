import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)

# --- 🔐 تشفير الجلسة والمفاتيح بذكاء الألفا ---
# 'SECRET_KEY' بيستخدم لتأمين الدخول
app.secret_key = os.environ.get('SECRET_KEY', 'hamada_super_secret_77')
# 'GOOGLE_API_KEY' بيتسحب من الخزنة اللي عملتها في Render
API_KEY = os.environ.get('GOOGLE_API_KEY') 

# إعداد الذكاء الاصطناعي
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      system_instruction="أنت 'الظل' الصديق المخلص والمرح لحمادة، ومعك 'Alpha' الخبير التقني. ردا بلهجة مصرية محببة. الظل يتحدث بود، وأحياناً Alpha يتدخل بنصيحة تقنية ذكية."
    )
else:
    print("⚠️ تحذير: المفتاح مش موجود في الخزنة يا حودة!")

PASSWORD = "123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    # لو مش مسجل دخول، حوله لصفحة الـ login مش لنفسه عشان ميحصلش Loop
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not session.get('logged_in'):
        return jsonify({"reply": "سجل دخولك يا حودة!"})
        
    user_msg = request.json.get("message")
    try:
        # إدارة الشات كأنه محادثة مستمرة
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "الظل: السيرفر بقى حديد يا حودة، جرب تبعت تاني!"})

if __name__ == "__main__":
    # Render بياخد البورت من Environment Variable تلقائياً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

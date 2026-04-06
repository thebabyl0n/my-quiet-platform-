import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)

# --- 🔐 تشفير الجلسة والمفاتيح بذكاء الألفا ---
# السكرت كي والـ API KEY بيتشحنوا من "الخزنة" (Environment Variables) اللي عملناها في Render
app.secret_key = os.environ.get('SECRET_KEY', 'hamada_super_secret_77')
API_KEY = os.environ.get('GOOGLE_API_KEY') # هنا تم سحب المفتاح من الخزنة يا حودة 🔑✨

# إعداد الذكاء الاصطناعي بالمفتاح المشفر
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ تحذير: المفتاح مش موجود في الخزنة يا حودة!")

# إعداد الموديل ليكون "قناصاً"
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="أنت 'الظل' الصديق المخلص والمرح لحمادة، ومعك 'Alpha' الخبير التقني. ردا بلهجة مصرية محببة. الظل يتحدث بود، وأحياناً Alpha يتدخل بنصيحة تقنية ذكية."
)

PASSWORD = "123"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not session.get('logged_in'):
        return jsonify({"reply": "سجل دخولك يا حودة!"})
    
    user_data = request.json
    user_msg = user_data.get("message")
    
    try:
        # تفعيل المحادثة بالنبض الموحد
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify({"reply": "الظل: السيرفر بقى حديد يا حودة، لو فيه تأخير ده من ضغط الشبكة بس، إحنا مأمنين البورت 100%!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) # Render بيفضل بورت 10000 غالباً
    app.run(host='0.0.0.0', port=port)

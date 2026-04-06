import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_key_hamada'

# إعداد المفتاح
API_KEY = "AIzaSyBFDDRMctvn8btilW6VXgQxJkvod_6hUZw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # استخدمنا نسخة أسرع وأخف

PASSWORD = "123"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
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
        return jsonify({"reply": "سجل دخول الأول يا حودة!"})
    
    user_msg = request.json.get("message")
    try:
        # بنطلب من الذكاء الاصطناعي يرد بشخصية الظل
        prompt = f"أنت الآن 'الظل' صديق حمادة المقرب. رد عليه بلهجة مصرية ودودة وقصيرة: {user_msg}"
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "الظل: معلش يا حودة، السيرفر لسه بيسخن، ابعت الكلمة دي تاني كدة؟"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'hamada_77_secret')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == "123":
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
        return jsonify({"reply": "سجل دخولك يا حودة!"})
        
    user_msg = request.json.get("message")
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    try:
        # بنشغل الـ API جوه الدالة عشان يقرأ المفتاح فريش
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(f"أنت 'الظل' صديق حمادة المخلص، رد بلهجة مصرية: {user_msg}")
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": "الظل: لسه فيه حاجة بسيطة معلقة في السيرفر، بس أنا معاك ومش هسيبك!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

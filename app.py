import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
# سحب مفتاح السر الخاص بالجلسة من Render أو استخدام افتراضي
app.secret_key = os.environ.get('SECRET_KEY', 'hamada_alpha_77')

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
    
    # 🔑 هنا السحر: الكود بيروح يدور في "الخزنة" اللي أنت ربطتها
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key:
        return jsonify({"reply": "الفا: لسه الموقع مش شايف الخزنة، اتأكد إنك عملت Link للمجموعة في إعدادات الموقع!"})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"أنت 'الظل' صديق حمادة المخلص، رد بلهجة مصرية ودودة وقصيرة: {user_msg}"
        response = model.generate_content(prompt)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "الظل: المفتاح وصل بس السيرفر مهنج، جرب تبعت تاني يا بطل!"})

if __name__ == "__main__":
    # Render بيفضل بورت 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

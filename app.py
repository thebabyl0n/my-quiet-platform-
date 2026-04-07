import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'hamada_alpha_77')

# سحب المفتاح
api_key = os.environ.get('GOOGLE_API_KEY')

if api_key:
    genai.configure(api_key=api_key)

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

    if not api_key:
        return jsonify({"reply": "الفا: السيرفر مش شايف GOOGLE_API_KEY!"})

    try:
        # التعديل هنا: بنحدد الموديل بوضوح ونتأكد من الـ Generation Config
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"typical_p": 0.95, "temperature": 0.7}
        )
        
        prompt = f"أنت 'الظل' صديق حمادة المخلص، رد بلهجة مصرية ودودة جداً: {user_msg}"
        
        # بنستخدم generate_content وبنضيف timeout احتياطي
        response = model.generate_content(prompt)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        # لو فشل، بنجرب نناديه بالاسم الكامل (الحل اللي في الصورة)
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(user_msg)
            return jsonify({"reply": response.text})
        except Exception as e2:
            return jsonify({"reply": f"الظل لسه بيعافر، الخطأ: {str(e2)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

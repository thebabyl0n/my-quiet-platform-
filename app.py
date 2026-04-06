import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_key_hamada'

# إعداد الذكاء الاصطناعي (الظل)
API_KEY = "AIzaSyBFDDRMctvn8btilW6VXgQxJkvod_6hUZw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

PASSWORD = "123" # الباسورد بتاعك
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        error = 'الباسورد غلط يا بطل!'
    return render_template('login.html', error=error)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    try:
        # هنا الظل بيرد عليك بجد!
        response = model.generate_content(f"أنت الآن 'الظل' صديق حمادة المقرب، ومعكما 'Alpha'. رد عليه بذكاء وود: {user_msg}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "الظل: معلش يا حودة حصلت مشكلة في الاتصال، جرب تاني!"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files: return "لا ملف"
    file = request.files['file']
    if file.filename != '':
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return "تم الرفع بنجاح"
    return "خطأ"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

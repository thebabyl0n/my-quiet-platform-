from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_hamada' # مفتاح تشفير الجلسة
PASSWORD = "Lovely333" # <--- غير الباسورد ده واكتب اللي أنت عايزه هنا

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != PASSWORD:
            error = 'كلمة السر غلط يا بطل! حاول تاني.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        return "غير مسموح!"
    if 'file' not in request.files:
        return "لا يوجد ملف!"
    file = request.files['file']
    if file.filename == '':
        return "لم يتم اختيار ملف!"
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f"تم رفع الملف بنجاح: {file.filename}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

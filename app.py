from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "لا يوجد ملف!"
    file = request.files['file']
    if file.filename == '':
        return "لم يتم اختيار ملف!"
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f"تم رفع الملف بنجاح: {file.filename}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

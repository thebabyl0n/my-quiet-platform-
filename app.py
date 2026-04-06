import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
# سرية الجلسة
app.secret_key = os.environ.get('SECRET_KEY', 'hamada_super_secret_77')

# إعداد الذكاء الاصطناعي بالمفتاح الجديد بتاعك
API_KEY = "AIzaSyCdRYEmkyEazIV_uiV7HcOJO6vP6OLWl9c"
genai.configure(api_key=API_KEY)

# إعداد الموديل
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
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify({"reply": "الظل: لسه فيه هزة بسيطة، جرب تبعت تاني يا حودة، إحنا ورا السيرفر والزمن طويل!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
from flask import Flask, render_template

app = Flask(__name__)

# 👑 دي الصفحة الوحيدة اللي السيرفر هيشوفها
@app.route('/')
def index():
    # السطر ده بيدور على index.html جوه فولدر templates
    return render_template('index.html')

# 🚫 لغينا الـ login خالص عشان الـ Error يختفي
@app.route('/login')
def redirect_to_home():
    from flask import redirect, url_for
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

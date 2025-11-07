from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = {}
subjects = {}
pages = {}
messages = []

@app.route('/')
def home():
    return "🌐 FriendNoteHub is running on your phone!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get("username")
    pwd = data.get("password")
    if name in users:
        return jsonify({"error": "User already exists"}), 400
    users[name] = pwd
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get("username")
    pwd = data.get("password")
    if name not in users or users[name] != pwd:
        return jsonify({"error": "Invalid credentials"}), 400
    return jsonify({"message": "Login successful!"})

@app.route('/subject', methods=['POST'])
def add_subject():
    data = request.get_json()
    user = data.get("username")
    sub = data.get("subject")
    subjects.setdefault(user, []).append(sub)
    return jsonify({"message": "Subject added!"})

@app.route('/subjects/<user>')
def get_subjects(user):
    return jsonify(subjects.get(user, []))

@app.route('/page', methods=['POST'])
def add_page():
    data = request.get_json()
    user = data.get("username")
    sub = data.get("subject")
    page_title = data.get("title")
    pages.setdefault((user, sub), []).append(page_title)
    return jsonify({"message": "Page added!"})

@app.route('/pages/<user>/<sub>')
def get_pages(user, sub):
    return jsonify(pages.get((user, sub), []))

@app.route('/chat', methods=['POST'])
def chat_send():
    data = request.get_json()
    user = data.get("username")
    text = data.get("text")
    messages.append({"user": user, "text": text})
    return jsonify({"message": "Sent!"})

@app.route('/chat')
def chat_get():
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


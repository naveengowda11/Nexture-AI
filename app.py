from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import timedelta
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'nghkosjgafeuonvgfiwtajdkj'
app.permanent_session_lifetime = timedelta(minutes=30)

# ---------- Database Setup ----------
DB_NAME = "nextureai.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS feedbacks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT,
                            feedback TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
    print("✅ Database initialized.")

# ---------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email and password:
        session.permanent = True
        session['email'] = email

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if not user:
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                conn.commit()

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html', email=session['email'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()

    if not user_message.strip():
        return jsonify({'response': "Please type something!"})

    # Simple AI logic
    if "hello" in user_message or "hi" in user_message:
        response = "Hello! How can I help you today?"
    elif "your name" in user_message:
        response = "I'm Nexture AI — your intelligent assistant!"
    elif "who made you" in user_message:
        response = "I was created by Naveen Kumar B and Yashwin Gowda K at Nexture AI!"
    elif "what can you do" in user_message:
        response = "I can help you to slove the problmes where feel difficulty, and will soon help with productivity tasks!"
    elif "thank you" in user_message:
        response = "You're welcome! 😊"
    elif "bye" in user_message:
        response = "Goodbye! Come back soon."
    elif "help" in user_message:
        response = "Sure! Ask me anything like 'what is AI', 'who created you', or just say hi."
    elif "ai" in user_message:
        response = "Artificial Intelligence is a field of computer science focused on creating smart machines that simulate human intelligence."
    elif "nexture" in user_message:
        response = "Nexture AI is your personalized productivity and learning assistant, built by passionate student developers."
    elif "devdutt padikal" in user_message:
        response = "indian crickter who is from karnataka"
    elif "sad" in user_message :
        response = "I'm really sorry you're feeling that way. I'm here for you. 💙"
    elif  "depressed" in user_message :
        response = "You're not alone. It’s okay to feel down sometimes. Sending you hugs 🤗"    
    elif  "happy" in user_message:   
        response= "Yay! I'm glad you're feeling great! 😊"
    elif  "angry" in user_message:
       response ="Take a deep breath... Want to talk about it?"
    elif  "anxious" in user_message:
        response = "It's okay. I'm here for you. Things will get better."
    elif  "lonely" in user_message :   
        response =  "You’re not alone. I’m with you. 💖"
    elif "excited" in user_message:   
        response="That's awesome! Tell me more.😄"        
    else:
        response = "Hmm, I didn't understand that yet. I'm still learning! 🤖"

    return jsonify({'response': response})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback = data.get('feedback', '')
    email = session.get('email', 'Anonymous')

    if feedback:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedbacks (email, feedback) VALUES (?, ?)", (email, feedback))
            conn.commit()
        return jsonify({"message": "Thanks for your feedback!"})
    else:
        return jsonify({"message": "Feedback cannot be empty."}), 400

@app.route('/view_feedbacks')
def view_feedbacks():
    if 'email' not in session:
        return redirect(url_for('index'))

    owner_email = 'navin@gmail.com'  # owners  email
    if session['email'] != owner_email:
        return "Access Denied: Only owner can view feedbacks.", 403

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email, feedback, timestamp FROM feedbacks ORDER BY timestamp DESC")
        feedback_list = cursor.fetchall()

    return render_template('view_feedbacks.html', feedbacks=feedback_list)

# ---------- Run App ----------
if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        init_db()
    app.run(debug=True)
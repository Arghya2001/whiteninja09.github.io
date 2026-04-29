from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuration using .env variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Achievement(db.Model):
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    issuer = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50))
    description = db.Column(db.Text)
    link = db.Column(db.String(200))

# Raw SQL helper
def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Routes
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM skills ORDER BY category, level DESC")
    skills = cursor.fetchall()

    cursor.execute("SELECT * FROM education ORDER BY year_range DESC")
    education = cursor.fetchall()

    cursor.close()
    conn.close()

    achievements = Achievement.query.all()

    return render_template('index.html',
                           projects=projects,
                           achievements=achievements,
                           skills=skills,
                           education=education)

@app.route('/admin/add-achievement', methods=['POST'])
def add_achievement():
    new_ach = Achievement(
        title=request.form['title'],
        issuer=request.form['issuer'],
        date=request.form['date'],
        description=request.form['description']
    )
    db.session.add(new_ach)
    db.session.commit()
    return "Achievement Added!"

@app.route('/save-message', methods=['POST'])
def save_message():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    conn = get_db()
    cursor = conn.cursor()
    query = "INSERT INTO contact_messages (name, email, phone, message) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, phone, message))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success", "message": "Thank you! I have received your message."})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
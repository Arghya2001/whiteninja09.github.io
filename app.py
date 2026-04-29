from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

app = Flask(__name__)

# 1. Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://arghya_user:Arghya2001@localhost/portfolio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Initialize Database (The unified way)
db = SQLAlchemy(app)

# 3. Define Models
class Achievement(db.Model):
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    issuer = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50))
    description = db.Column(db.Text)
    link = db.Column(db.String(200))

# 4. Helper for Raw SQL (Projects, Skills, Education)
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="arghya_user",
        password="Arghya2001",
        database="portfolio_db"
    )

# 5. Routes
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Raw SQL Queries
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM skills ORDER BY category, level DESC")
    skills = cursor.fetchall()
    
    cursor.execute("SELECT * FROM education ORDER BY year_range DESC")
    education = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # SQLAlchemy Query
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
    # Create database tables automatically if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta

# IST = UTC + 5:30
IST = timezone(timedelta(hours=5, minutes=30))

load_dotenv()

app = Flask(__name__)

# Configuration
DB_HOST     = os.getenv('DB_HOST')
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME     = os.getenv('DB_NAME')
DB_PORT     = os.getenv('DB_PORT', '3306')

# Secret key for session
app.secret_key = os.getenv('SECRET_KEY', 'arghya-admin-secret-123')

# Admin credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'arghya2001')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 280,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)

# ─── Models ───────────────────────────────────────────

class Achievement(db.Model):
    __tablename__ = 'achievement'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    issuer      = db.Column(db.String(100), nullable=False)
    date        = db.Column(db.String(50))
    description = db.Column(db.Text)
    link        = db.Column(db.String(200))

class Project(db.Model):
    __tablename__ = 'projects'
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(100))
    description  = db.Column(db.Text)
    tech_stack   = db.Column(db.String(255))
    project_link = db.Column(db.String(255))

class Skill(db.Model):
    __tablename__ = 'skills'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(50))
    category = db.Column(db.String(50))
    level    = db.Column(db.Integer)

class Education(db.Model):
    __tablename__ = 'education'
    id           = db.Column(db.Integer, primary_key=True)
    institution  = db.Column(db.String(100))
    degree       = db.Column(db.String(100))
    year_range   = db.Column(db.String(50))
    percentage   = db.Column(db.String(100))
    website_link = db.Column(db.String(255))

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(100), nullable=False)
    phone      = db.Column(db.String(10), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# ─── Routes ───────────────────────────────────────────

@app.route('/')
def index():
    projects     = Project.query.all()
    skills       = Skill.query.order_by(Skill.category, Skill.level.desc()).all()
    education    = Education.query.order_by(Education.year_range.desc()).all()
    achievements = Achievement.query.all()
    return render_template('index.html',
                           projects=projects,
                           achievements=achievements,
                           skills=skills,
                           education=education)

@app.route('/save-message', methods=['POST'])
def save_message():
    new_msg = ContactMessage(
        name    = request.form.get('name'),
        email   = request.form.get('email'),
        phone   = request.form.get('phone'),
        message = request.form.get('message')
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({"status": "success", "message": "Thank you! I have received your message."})

# ─── Admin Login ───────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_messages'))
        else:
            error = 'Wrong username or password!'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# ─── Admin Messages ────────────────────────────────────

@app.route('/admin/messages')
def admin_messages():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/delete-message/<int:id>')
def delete_message(id):
    if not session.get('admin_logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"})
    try:
        msg = ContactMessage.query.get_or_404(id)
        db.session.delete(msg)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})

@app.route('/admin/add-achievement', methods=['POST'])
def add_achievement():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    new_ach = Achievement(
        title       = request.form['title'],
        issuer      = request.form['issuer'],
        date        = request.form['date'],
        description = request.form['description'],
        link        = request.form.get('link')
    )
    db.session.add(new_ach)
    db.session.commit()
    return "Achievement Added!"

@app.template_filter('ist_time')
def ist_time_filter(dt):
    if dt is None:
        return 'N/A'
    ist_dt = dt.replace(tzinfo=timezone.utc).astimezone(IST)
    return ist_dt.strftime('%d %b %Y, %I:%M %p')

# ─── Run ──────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
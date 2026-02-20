from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
# Configuración
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chismografo-secreto-super-seguro')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chismes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS DE BASE DE DATOS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    messages = db.relationship('Message', backref='author', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- RUTAS ---

@app.route('/')
@login_required 
def index():
    # Obtener todos los mensajes ordenados por fecha (más reciente primero)
    all_messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', messages=all_messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('¡Bienvenido al chisme!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos. ¡Inténtalo de nuevo!', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username').lower().strip()
        password = request.form.get('password')
        
        # Verificar si el usuario ya existe
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Este nombre de usuario ya está apartado. ¡Elige otro!', 'error')
            return redirect(url_for('register'))
        
        # Crear nuevo usuario con hash de contraseña
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('¡Cuenta creada! Ya eres parte del Chismógrafo.', 'success')
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Adiós! Regresa cuando tengas más chismes.', 'info')
    return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
@login_required
def post_message():
    content = request.form.get('content')
    if content:
        new_msg = Message(content=content, author=current_user)
        db.session.add(new_msg)
        db.session.commit()
        flash('¡Chisme publicado!', 'success')
    return redirect(url_for('index'))

# Inicializar la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("logs/app.log"),  # Grava logs em um arquivo chamado app.log
                        logging.StreamHandler()          # Exibe logs no console
                    ]
                    )

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()
    # Criar usuários iniciais
    if not User.query.filter_by(email='user1@email.com').first():
        user1 = User(email='user1@email.com')
        user1.set_password('password1')
        db.session.add(user1)
    if not User.query.filter_by(email='user2@mail.io').first():
        user2 = User(email='user2@mail.io')
        user2.set_password('password2')
        db.session.add(user2)
    db.session.commit()

@app.route('/')
def index():
    logging.debug('Accessing /index route')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    todos = Todo.query.filter_by(user_id=user.id).all()
    logging.info(f'User {user.email} accessed their task list.')
    return render_template('index.html', todos=todos, email=user.email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug('Accessing /login route')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar se o usuário existe
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login realizado com sucesso!', 'success')
            logging.info(f'User {email} successfully logged in.')
            return redirect(url_for('index'))
        else:
            logging.info(f'Failed login attempt for email {email}')
            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logging.debug('Accessing /logout route')
    user_id = session.pop('user_id', None)
    logging.info(f'User {user_id} logged out.')
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    logging.debug('Accessing /add route')
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar tarefas.', 'error')
        logging.info('Add task attempted without login.')
        return redirect(url_for('login'))

    content = request.form['content']
    if not content:
        flash("Erro: Campo de tarefa vazio!", "error")
        logging.info('Empty task submission attempted.')
        return redirect(url_for('index'))
    
    new_todo = Todo(content=content, user_id=session['user_id'])

    try:
        db.session.add(new_todo)
        db.session.commit()
        flash('Tarefa adicionada!', 'success')
        logging.info(f"Task '{content}' added by user {session['user_id']}")
        return redirect(url_for('index'))
    except Exception as e:
        flash('Erro ao adicionar tarefa!', 'error')
        logging.error(f'Error adding task by user {session["user_id"]}: {e}')
        return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    logging.debug('Accessing /complete route')
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Por favor, faça login para completar tarefas.', 'category': 'error'}), 401  # 401 Unauthorized

    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        logging.warning(f'Unauthorized attempt to complete task {id} by user {session["user_id"]}')
        return jsonify({'status': 'error', 'message': 'Você não tem permissão para alterar esta tarefa.', 'category': 'error'}), 403  # 403 Forbidden

    data = request.get_json()
    todo.completed = data.get('completed', False)

    try:
        db.session.commit()
        message = 'Parabéns por concluir a tarefa!' if todo.completed else 'Tarefa desmarcada como não concluída.'
        logging.info(f'Task {id} marked {"completed" if todo.completed else "not completed"} by user {session["user_id"]}')
        return jsonify({'status': 'success', 'message': message, 'category': 'success'})
    except Exception as e:
        logging.error(f'Error completing task {id} by user {session["user_id"]}: {e}')
        return jsonify({'status': 'error', 'message': 'Erro ao atualizar tarefa.', 'category': 'error'}), 500  # 500 Internal Server Error

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    logging.debug('Accessing /delete route')
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Por favor, faça login para excluir tarefas.', 'category': 'error'}), 401  # 401 Unauthorized

    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        logging.warning(f'Unauthorized delete attempt on task {id} by user {session["user_id"]}')
        return jsonify({'status': 'error', 'message': 'Você não tem permissão para excluir esta tarefa.', 'category': 'error'}), 403  # 403 Forbidden

    try:
        db.session.delete(todo)
        db.session.commit()
        logging.info(f'Task {id} deleted by user {session["user_id"]}')
        return jsonify({'status': 'success', 'message': 'Tarefa excluída!', 'category': 'success'})
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error deleting task {id} by user {session["user_id"]}: {e}')
        return jsonify({'status': 'error', 'message': 'Erro ao excluir tarefa.', 'category': 'error'}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    logging.debug('Accessing register route')
    #se for metodo POST, extrair email e senha e confirmar senha
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        #senhas coincidem?
        if password != confirm_password:
            flash('Os passwords não coincidem', 'error')
            return redirect(url_for('register'))
        #usuario ja existe?
        if email == User.query.filter_by(email=email).first():
            flash('Este email já se encontra em uso. Tente outro', 'error')
            return redirect(url_for('register'))
        #criar novo user
        new_user = User(email=email)
        new_user.set_password(password)
        #try add ao db
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário registrado com sucesso!', 'success')
            logging.info(f'New user registered: {email}')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar novo usuário', 'error')
            logging.error(f'Error registering user: {e}')
            return redirect(url_for('register'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
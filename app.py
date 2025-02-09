from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    todos = Todo.query.filter_by(user_id=user.id).all()
    return render_template('index.html', todos=todos, email=user.email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar se o usuário existe
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha inválidos.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        flash('Por favor, faça login para adicionar tarefas.', 'error')
        return redirect(url_for('login'))

    content = request.form['content']
    if not content:
        flash("Erro: Campo de tarefa vazio!", "error")
        return redirect(url_for('index'))
    
    new_todo = Todo(content=content, user_id=session['user_id'])

    try:
        db.session.add(new_todo)
        db.session.commit()
        flash('Tarefa adicionada!', 'success')
        return redirect(url_for('index'))
    except:
        flash('Erro ao adicionar tarefa!', 'error')
        return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Por favor, faça login para completar tarefas.', 'category': 'error'}), 401  # 401 Unauthorized

    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'Você não tem permissão para alterar esta tarefa.', 'category': 'error'}), 403  # 403 Forbidden

    data = request.get_json()
    todo.completed = data.get('completed', False)

    try:
        db.session.commit()
        message = 'Parabéns por concluir a tarefa!' if todo.completed else 'Tarefa desmarcada como não concluída.'
        return jsonify({'status': 'success', 'message': message, 'category': 'success'})
    except:
        return jsonify({'status': 'error', 'message': 'Erro ao atualizar tarefa.', 'category': 'error'}), 500  # 500 Internal Server Error

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Por favor, faça login para excluir tarefas.', 'category': 'error'}), 401  # 401 Unauthorized

    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'Você não tem permissão para excluir esta tarefa.', 'category': 'error'}), 403  # 403 Forbidden

    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Tarefa excluída!', 'category': 'success'})
    except:
        return jsonify({'status': 'error', 'message': 'Erro ao excluir tarefa.', 'category': 'error'}), 500  # 500 Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)



# PROXIMOS PASSOS: 1- CRIAR LOGS | 2- MAIS LISTAS POR USUÁRIO | 3- UMA LISTA POR DIA (ENVOLVER CALENDÁRIO)
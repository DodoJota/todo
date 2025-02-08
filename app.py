from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relacionamento com o usuário
    user = db.relationship('User', backref=db.backref('todos', lazy=True))
    # Relacionamento com a lista
    task_list = db.relationship('TaskList', backref=db.backref('todos', lazy=True))

class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relacionamento com o usuário
    user = db.relationship('User', backref=db.backref('task_lists', lazy=True))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_todo = Todo(content=content, user_id=current_user.id)

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
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    todo.completed = data.get('completed', False)

    try:
        db.session.commit()
        message = 'Parabéns por concluir a tarefa!' if todo.completed else 'Tarefa desmarcada como não concluída.'
        return jsonify({'status': 'success', 'message': message, 'category': 'success'})
    except:
        return jsonify({'status': 'error', 'message': 'Erro ao atualizar tarefa.', 'category': 'error'}), 500

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Tarefa excluída!', 'category': 'success'})
    except:
        return jsonify({'status': 'error', 'message': 'Erro ao excluir tarefa.', 'category': 'error'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
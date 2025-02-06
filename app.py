from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template(index.html, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    content = request.form('content')
    new_todo = Todo(content=content)

    try:
        db.session.add(new_todo)
        db.session.commit()
        flash('Tarefa adicionada!','success')
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
        return jsonify({'status': 'success', 'message': message})
    except:
         return jsonify({'status': 'error'}), 500

@app.route('/delete/<int:id>', methods=['POST'])
def delete():
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Tarefa excluída!', 'success')
        return redirect(url_for('index'))
    except:
        flash('Erro ao excluir tarefa', 'error')
        return redirect(url_for('index'))

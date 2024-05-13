# Importação dos módulos necessários
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# Criando uma instância do Flask
app = Flask(__name__, template_folder='templates')

# Configurando um banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.sqlite3'

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Definindo o modelo de dados
class Estudante(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
# Definindo a rota
@app.route('/')
def index():
    estudantes = Estudante.query.all()
    return render_template('index.html', estudantes=estudantes)

# Definindo a rota add
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        estudante = Estudante(nome, idade)
        db.session.add(estudante)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Definindo a rota de editar alunos
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    estudante = Estudante.query.get(id)
    if request.method == 'POST':
        estudante.nome = request.form['nome']
        estudante.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', estudante=estudante)

# Definindo a rota de excluir alunos
@app.route('/delete/<int:id>')
def delete(id):
    estudante = Estudante.query.get(id)
    db.session.delete(estudante)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
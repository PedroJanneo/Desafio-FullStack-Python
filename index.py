from flask import Flask, redirect, render_template, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.secret_key = 'desafioPython'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://root:@localhost/to-do-list'
)

db = SQLAlchemy(app)

class Tarefas(db.Model):
    idTarefa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tarefa = db.Column(db.String(50), nullable=False)
    statusTarefa = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<Tarefa %r>' % self.tarefa
    
@app.route('/inicio')
def ola():
    return "<h1> Iniciando o flask </h1>"

@app.route("/lista")
def lista():
    lista_tarefas = Tarefas.query.order_by(Tarefas.idTarefa).all()
    return render_template('listaTarefas.html', 
                           descricao='Aqui estão as tarefas registradas', 
                           listaTaref=lista_tarefas)

@app.route("/cadastrarTarefa")
def cadastrar_tarefa():
    return render_template("cadastrarTarefa.html")

@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    tarefaP = request.form['txtTarefa']
    statusP = request.form['txtStatus']

    tarefa_adicionado = Tarefas(tarefa=tarefaP, statusTarefa=statusP)

    db.session.add(tarefa_adicionado)
    db.session.commit()

    flash("Tarefa adicionada", "success")
    return redirect('/lista')

@app.route('/editar/<int:id>')
def editar_status(id):
    tarefa_selecionada = Tarefas.query.filter_by(idTarefa=id).first()
    return render_template('editar.html', tarefa=tarefa_selecionada)

@app.route('/atualizar', methods=['POST'])
def atualizar_status():
    tarefa = Tarefas.query.filter_by(idTarefa=request.form['txtId']).first()
    tarefa.statusTarefa = request.form['txtStatus']

    db.session.commit()
    flash("Status da tarefa atualizada", "success")
    return redirect("/lista")

@app.route("/excluir/<int:id>")
def excluir_tarefa(id):
    Tarefas.query.filter_by(idTarefa=id).delete()
    db.session.commit()
    flash("Tarefa deletada", "error")
    return redirect("/lista")

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST']) 
def autenticar():
    login = request.form['txtLogin']
    senha = request.form['txtSenha']

    if login == 'admin' and senha == 'admin':
        session['usuario_logado'] = login
        flash("Usuário logado com sucesso", "success")
        return redirect("/lista")
    else:
        flash("Login ou senha incorretos", "error")
        return redirect('/login')


app.run()

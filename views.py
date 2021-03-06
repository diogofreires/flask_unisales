from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Curso
from dao import CursoDao, UsuarioDao
import time
from helpers import deleta_arquivo, recupera_imagem
from curso import db, app

curso_dao = CursoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/index')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    lista = curso_dao.listar()
    return render_template('lista.html', titulo='Cursos', cursos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Curso')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    duracao = request.form['duracao']
    curso = Curso(nome, categoria, duracao)
    curso = curso_dao.salvar(curso)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{curso.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    curso = curso_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Curso', curso=curso, capa_curso=nome_imagem or 'capa_padrao.jpg')


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    duracao = request.form['duracao']
    curso = Curso(nome, categoria, duracao, id=request.form['id'])

    arquivo = request.files['arquivo']
    if arquivo:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(curso.id)
        arquivo.save(f'{upload_path}/capa{curso.id}-{timestamp}.jpg')
    curso_dao.salvar(curso)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('deletar')))
    curso_dao.deletar(id)
    flash('O curso foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        elif usuario.senha != request.form['senha']:
            flash('Usu??rio ou Senha incorreto. Tente novamente!')
            return redirect(url_for('login'))
    else:
        flash('Usu??rio ou Senha incorreto. Tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usu??rio logado!')
    return redirect(url_for('login'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('imagem')))
    return send_from_directory('uploads', nome_arquivo)

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database
from database import *

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get('nome')
        gmail = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not gmail or not senha:
            return flash("você precisa digitar o nome, email e senha")
            

        
        pessoa = database.buscar_usuario_por_email(gmail)
        if pessoa:
            flash("você precisa informar um email diferente de um ja existente")
            return redirect(url_for('auth.registro'))

        hash = generate_password_hash(senha)
        database.criar_usuario(nome, gmail, hash)


        
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gmail = request.form.get('email')
        senha = request.form.get('senha')

        if not gmail or not senha:
            flash("forneça o email e a senha")
            return redirect(url_for('auth.login'))

        
        usuario = database.buscar_usuario_por_email(gmail)
        
        if not usuario or not check_password_hash(usuario.senha_hash, senha):
            flash("email ou senhas invalidas")
            return redirect(url_for('auth.login'))

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        
       
        return redirect(url_for("leituras.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("usuario_nome", None)
    
    return redirect(url_for("auth.login"))

# routes/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('index.html')

@main_bp.route('/monitor')
def monitor():
    """Página de monitoramento em tempo real"""
    return render_template('monitor.html')

@main_bp.route('/users')
def users():
    """Página de gerenciamento de usuários"""
    return render_template('users.html')

@main_bp.route('/logs')
def logs():
    """Página de logs de acesso"""
    return render_template('logs.html')
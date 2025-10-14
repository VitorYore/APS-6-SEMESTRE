# routes/api.py
from flask import Blueprint, jsonify, request
import base64
import os
from datetime import datetime
from utils.database import (
    clear_logs, load_users, add_user, delete_user, 
    load_logs, get_stats
)
from utils.face_recognition import get_current_status, reload_users
from utils.config import PHOTOS_DIR

api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
def status():
    """Retorna status atual do sistema"""
    return jsonify(get_current_status())

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Lista todos os usuários"""
    users = load_users()
    # Remove embeddings para não sobrecarregar resposta
    return jsonify([{k: v for k, v in u.items() if k != 'embedding'} for u in users])

@api_bp.route('/users', methods=['POST'])
def create_user():
    """Cadastra novo usuário"""
    try:
        data = request.get_json()
        
        # Valida dados
        if not data.get('name') or not data.get('access_level') or not data.get('photo'):
            return jsonify({'success': False, 'message': 'Dados incompletos'}), 400
        
        # Salva foto
        img_data = data['photo'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        filename = f"{data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(PHOTOS_DIR, filename)
        
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        
        # Adiciona usuário ao banco
        add_user(data['name'], data['access_level'], filename)
        
        # Mensagem de sucesso
        print(f"✅ Usuário {data['name']} cadastrado com sucesso!")
        
        return jsonify({
            'success': True, 
            'message': f'Usuário {data["name"]} cadastrado! Por favor, reinicie o servidor para carregar os embeddings.'
        })
        
    except Exception as e:
        print(f"❌ Erro ao cadastrar usuário: {e}")
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500

@api_bp.route('/users', methods=['DELETE'])
def remove_user():
    """Remove usuário"""
    try:
        user_name = request.args.get('name')
        
        if not user_name:
            return jsonify({'success': False, 'message': 'Nome não fornecido'}), 400
        
        delete_user(user_name)
        reload_users()
        
        return jsonify({
            'success': True, 
            'message': f'Usuário {user_name} removido com sucesso!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/logs')
def get_logs():
    """Retorna logs de acesso"""
    logs = load_logs()
    return jsonify(logs[-50:])  # Últimos 50 registros

@api_bp.route('/logs', methods=['DELETE'])
def delete_logs():
    """Apaga todos os logs"""
    try:
        clear_logs()
        return jsonify({
            'success': True,
            'message': 'Todos os logs foram apagados com sucesso!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao apagar logs: {str(e)}'
        }), 500


@api_bp.route('/stats')
def statistics():
    """Retorna estatísticas do sistema"""
    return jsonify(get_stats())

@api_bp.route('/reload', methods=['POST'])
def reload():
    """Recarrega embeddings dos usuários"""
    try:
        reload_users()
        return jsonify({
            'success': True,
            'message': 'Embeddings recarregados com sucesso!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao recarregar: {str(e)}'
        }), 500
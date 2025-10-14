# utils/database.py
import json
import os
from datetime import datetime
from utils.config import USERS_FILE, LOG_FILE, MAX_LOGS

def load_users():
    """Carrega usuários do arquivo JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_users(users):
    """Salva usuários no arquivo JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def add_user(name, access_level, img_filename):
    """Adiciona novo usuário"""
    users = load_users()
    
    # Verificação de duplicidade
    for u in users:
        if u['name'].strip().lower() == name.strip().lower():
            raise ValueError(f"O usuário '{name}' já está cadastrado.")
        
    users.append({
        'name': name,
        'access_level': int(access_level),
        'img_filename': img_filename,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_users(users)
    return True

def delete_user(name):
    """Remove usuário"""
    users = load_users()
    users = [u for u in users if u['name'] != name]
    save_users(users)
    return True

def load_logs():
    """Carrega logs de acesso"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:  # arquivo vazio
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"⚠️  JSON inválido em {LOG_FILE}, reiniciando...")
            return []
    return []

def save_log(log_entry):
    """Adiciona entrada ao log"""
    logs = load_logs()
    logs.append(log_entry)
    
    # Mantém apenas os últimos MAX_LOGS registros
    logs = logs[-MAX_LOGS:]
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
    
def clear_logs():
    """Apaga todos os logs"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("[]")  # arquivo JSON vazio


def get_stats():
    """Retorna estatísticas do sistema"""
    logs = load_logs()
    users = load_users()
    
    total = len(logs)
    authorized = len([l for l in logs if l['status'] == 'AUTORIZADO'])
    denied = total - authorized
    
    return {
        'total_attempts': total,
        'authorized': authorized,
        'denied': denied,
        'users_registered': len(users)
    }
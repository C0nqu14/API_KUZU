from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models import User 

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user) 
        return jsonify({"message": "Login bem-sucedido", "user": user.to_dict()}), 200
    else:
        return jsonify({"message": "Nome de usuário ou senha inválidos"}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user() 
    return jsonify({"message": "Logout bem-sucedido"}), 200

@auth_bp.route('/status', methods=['GET'])
@login_required
def status():
    return jsonify({"message": "Usuário logado", "user": current_user.to_dict()}), 200

@auth_bp.route('/protected', methods=['GET'])
@login_required
def protected_route():
    return jsonify({"message": f"Olá, {current_user.username}! Você acessou uma rota protegida."}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user') 

    if not username or not password:
        return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Nome de usuário já existe"}), 409

    new_user = User(username=username, role=role)
    new_user.set_password(password) 

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário registrado com sucesso", "user": new_user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
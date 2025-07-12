from flask import Blueprint, jsonify, request
from extensions import db
from models import Ocorrencia, Detento 

ocorrencias_bp = Blueprint('ocorrencias', __name__, url_prefix='/api/ocorrencias')

@ocorrencias_bp.route('/', methods=['GET'])
def get_ocorrencias():
    ocorrencias = Ocorrencia.query.all()
    return jsonify([ocorrencia.to_dict() for ocorrencia in ocorrencias])

@ocorrencias_bp.route('/', methods=['POST'])
def add_ocorrencia():
    data = request.get_json()
    if not data or not data.get('titulo') or not data.get('tipo'):
        return jsonify({"error": "Título e Tipo são obrigatórios para Ocorrência"}), 400

    new_ocorrencia = Ocorrencia(
        titulo=data['titulo'],
        descricao=data.get('descricao'),
        local=data.get('local'),
        tipo=data['tipo'],
        detento_id=data.get('detento_id')
    )

    try:
        db.session.add(new_ocorrencia)
        db.session.commit()
        return jsonify(new_ocorrencia.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
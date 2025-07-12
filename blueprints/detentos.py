from flask import Blueprint, jsonify, request
from extensions import db
from models import Detento

detentos_bp = Blueprint('detentos', __name__, url_prefix='/api/detentos')

@detentos_bp.route('/', methods=['GET'])
def get_detentos():
    detentos = Detento.query.all()
    return jsonify([detento.to_dict() for detento in detentos])

@detentos_bp.route('/', methods=['POST'])
def add_detento():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado JSON fornecido"}), 400

    if not data.get('nome') or not data.get('periculosidade'):
        return jsonify({"error": "Nome e Periculosidade são campos obrigatórios"}), 400

    new_detento = Detento(
        nome=data['nome'],
        idade=data.get('idade'),
        crimes_cometidos=data.get('crimes_cometidos'),
        sentenca=data.get('sentenca'),
        status=data.get('status'),
        periculosidade=data['periculosidade'],
        historico_movimentacoes=data.get('historico_movimentacoes'),
        foto_url=data.get('foto_url')
    )

    try:
        db.session.add(new_detento)
        db.session.commit()
        return jsonify(new_detento.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@detentos_bp.route('/<int:detento_id>', methods=['GET'])
def get_detento(detento_id):
    detento = Detento.query.get_or_404(detento_id)
    return jsonify(detento.to_dict())

@detentos_bp.route('/<int:detento_id>', methods=['PUT'])
def update_detento(detento_id):
    detento = Detento.query.get_or_404(detento_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado JSON fornecido"}), 400

    detento.nome = data.get('nome', detento.nome)
    detento.idade = data.get('idade', detento.idade)
    detento.crimes_cometidos = data.get('crimes_cometidos', detento.crimes_cometidos)
    detento.sentenca = data.get('sentenca', detento.sentenca)
    detento.status = data.get('status', detento.status)
    detento.periculosidade = data.get('periculosidade', detento.periculosidade)
    detento.historico_movimentacoes = data.get('historico_movimentacoes', detento.historico_movimentacoes)
    detento.foto_url = data.get('foto_url', detento.foto_url)

    try:
        db.session.commit()
        return jsonify(detento.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@detentos_bp.route('/<int:detento_id>', methods=['DELETE'])
def delete_detento(detento_id):
    detento = Detento.query.get_or_404(detento_id)
    try:
        db.session.delete(detento)
        db.session.commit()
        return jsonify({"message": "Detento excluído com sucesso"}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
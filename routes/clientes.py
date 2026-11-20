from flask import Blueprint, jsonify, request
from database import db
from models import Cliente, Locacao

clientes_bp = Blueprint('clientes_bp', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        "id": c.id, "nome": c.nome, "cpf": c.cpf, "telefone": c.telefone, "email": c.email
    } for c in clientes])

@clientes_bp.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.get_json()
    novo = Cliente(
        nome=dados.get('nome'),
        cpf=dados.get('cpf'),
        telefone=dados.get('telefone'),
        email=dados.get('email')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Cliente cadastrado com sucesso", "id": novo.id}), 201

@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    # Verifica se existe APENAS locação em aberto (não devolvida)
    locacao_ativa = Locacao.query.filter_by(id_cliente=id, devolvida=False).first()
    if locacao_ativa:
        return jsonify({"erro": "Não é possível excluir um cliente com locações ativas."}), 400

    # Se todas as locações já foram devolvidas, permite a exclusão
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente excluído com sucesso."}), 200
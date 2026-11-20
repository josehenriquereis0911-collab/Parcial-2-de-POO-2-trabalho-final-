from flask import Blueprint, jsonify, request
from database import db
from models import Locacao, Filme
from datetime import datetime, timedelta

locadora_bp = Blueprint('locadora_bp', __name__)

@locadora_bp.route('/locacoes', methods=['GET'])
def listar_locacoes():
    locacoes = Locacao.query.all()
    resultado = []
    for l in locacoes:
        resultado.append({
            "id": l.id,
            "cliente": l.cliente.nome,
            "cpf": l.cliente.cpf,
            "filme": l.filme.titulo,
            "classificacao": l.filme.classificacao,
            "data_locacao": l.data_locacao.strftime("%Y-%m-%d"),
            "data_prevista": l.data_prevista.strftime("%Y-%m-%d"),
            "devolvida": l.devolvida
        })
    return jsonify(resultado)

@locadora_bp.route('/locacoes', methods=['POST'])
def criar_locacao():
    dados = request.get_json()
    id_cliente = dados.get('id_cliente')
    id_filme = dados.get('id_filme')
    dias = dados.get('dias', 7)

    filme = Filme.query.get_or_404(id_filme)
    if filme.quantidade <= 0:
        return jsonify({"erro": "Filme esgotado"}), 400

    hoje = datetime.now().date()
    prevista = hoje + timedelta(days=dias)

    nova = Locacao(
        id_cliente=id_cliente,
        id_filme=id_filme,
        data_locacao=hoje,
        data_prevista=prevista,
        devolvida=False
    )
    filme.quantidade -= 1

    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Locação registrada com sucesso"}), 201

@locadora_bp.route('/locacoes/<int:id>/devolver', methods=['PUT'])
def devolver_locacao(id):
    locacao = Locacao.query.get_or_404(id)
    if locacao.devolvida:
        return jsonify({"erro": "Locação já devolvida"}), 400

    locacao.devolvida = True
    locacao.filme.quantidade += 1
    db.session.commit()
    return jsonify({"mensagem": "Devolução registrada com sucesso"})
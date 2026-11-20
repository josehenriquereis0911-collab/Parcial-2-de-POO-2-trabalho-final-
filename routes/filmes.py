from flask import Blueprint, jsonify, request
from database import db
from models import Filme, Locacao

filmes_bp = Blueprint('filmes_bp', __name__)

@filmes_bp.route('/filmes', methods=['GET'])
def listar_filmes():
    filmes = Filme.query.all()
    return jsonify([{
        "id": f.id, "titulo": f.titulo, "genero": f.genero,
        "diretor": f.diretor, "quantidade": f.quantidade, "classificacao": f.classificacao
    } for f in filmes])

@filmes_bp.route('/filmes', methods=['POST'])
def cadastrar_filme():
    dados = request.get_json()
    novo = Filme(
        titulo=dados.get('titulo'),
        genero=dados.get('genero'),
        diretor=dados.get('diretor'),
        quantidade=dados.get('quantidade', 1),
        classificacao=dados.get('classificacao')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Filme cadastrado com sucesso", "id": novo.id}), 201

@filmes_bp.route('/filmes/<int:id>', methods=['DELETE'])
def excluir_filme(id):
    filme = Filme.query.get_or_404(id)
    
    # Verifica se existe APENAS locação em aberto (não devolvida) para este filme
    locacao_ativa = Locacao.query.filter_by(id_filme=id, devolvida=False).first()
    if locacao_ativa:
        return jsonify({"erro": "Não é possível excluir um filme que possui locações ativas em aberto."}), 400

    # Se houver locações antigas já devolvidas, limpamos o histórico delas 
    # para evitar erro de chave estrangeira (IntegrityError) no banco de dados:
    Locacao.query.filter_by(id_filme=id).delete()

    # Agora removemos o filme com segurança
    db.session.delete(filme)
    db.session.commit()
    return jsonify({"mensagem": "Filme excluído com sucesso."}), 200
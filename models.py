from database import db

class Filme(db.Model):
    __tablename__ = 'filmes'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    diretor = db.Column(db.String(100))
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    classificacao = db.Column(db.String(20))

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Locacao(db.Model):
    __tablename__ = 'locacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    id_filme = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=False)
    data_locacao = db.Column(db.Date, nullable=False)
    data_prevista = db.Column(db.Date, nullable=False)
    devolvida = db.Column(db.Boolean, nullable=False, default=False)

    cliente = db.relationship('Cliente', backref='locacoes')
    filme = db.relationship('Filme', backref='locacoes')
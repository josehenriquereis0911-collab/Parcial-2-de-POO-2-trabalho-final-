import os
from flask import Flask
from database import db
from routes.clientes import clientes_bp
from routes.filmes import filmes_bp
from routes.locadora import locadora_bp

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'locadora.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registro dos Blueprints
app.register_blueprint(clientes_bp)
app.register_blueprint(filmes_bp)
app.register_blueprint(locadora_bp)

@app.route('/')
def index():
    return {"status": "API da Locadora Rodando com SQLite com Sucesso!"}

# Cria as tabelas automaticamente ao iniciar (substitui o init.sql do Postgres)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
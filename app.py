from flask import Flask, jsonify
from config import Config
from extensions import db, cors, login_manager 


from blueprints.detentos import detentos_bp
from blueprints.ocorrencias import ocorrencias_bp
from blueprints.dashboard import dashboard_bp
from blueprints.auth import auth_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app) 
    login_manager.login_view = 'auth.login'

    app.register_blueprint(detentos_bp)
    app.register_blueprint(ocorrencias_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp) 

    @app.route('/')
    def hello_world():
        return jsonify(message="Bem-vindo à API Kuzú!")

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

        
        from models import Detento, User 
        if not User.query.filter_by(username='admin').first():
            print("Criando usuário administrador padrão...")
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123') 
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário 'admin' criado com sucesso.")

        if not Detento.query.first():
            print("Adicionando dados de exemplo de detentos...")
            detento1 = Detento(nome='João Matador', idade=45, crimes_cometidos='Assassinato', sentenca='Prisão perpétua', status='Preso', periculosidade='Alta', historico_movimentacoes='01/01/2020: Preso', foto_url='https://example.com/joao.jpg')
            detento2 = Detento(nome='Edgar Mata', idade=30, crimes_cometidos='Violação, Sequestro', sentenca='20 anos', status='Foragido', periculosidade='Alta', historico_movimentacoes='15/03/2023: Fugiu da prisão', foto_url='https://example.com/edgar.jpg')
            detento3 = Detento(nome='Samuel Pica', idade=25, crimes_cometidos='Roubo', sentenca='5 anos', status='Condicional', periculosidade='Média', historico_movimentacoes='10/05/2024: Liberdade condicional', foto_url='https://example.com/samuel.jpg')
            db.session.add_all([detento1, detento2, detento3])
            db.session.commit()
            print("Dados de exemplo de detentos adicionados.")

    app.run(debug=True)
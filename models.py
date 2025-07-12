from extensions import db
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash 

class Detento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    crimes_cometidos = db.Column(db.Text)
    sentenca = db.Column(db.String(255))
    status = db.Column(db.String(50)) 
    periculosidade = db.Column(db.String(50))
    historico_movimentacoes = db.Column(db.Text)
    foto_url = db.Column(db.String(255)) 

    def __repr__(self):
        return f'<Detento {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'crimes_cometidos': self.crimes_cometidos,
            'sentenca': self.sentenca,
            'status': self.status,
            'periculosidade': self.periculosidade,
            'historico_movimentacoes': self.historico_movimentacoes,
            'foto_url': self.foto_url
        }

class Ocorrencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data = db.Column(db.DateTime, default=db.func.current_timestamp())
    local = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    detento_id = db.Column(db.Integer, db.ForeignKey('detento.id'), nullable=True)

    detento = db.relationship('Detento', backref=db.backref('ocorrencias', lazy=True))

    def __repr__(self):
        return f'<Ocorrencia {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data': self.data.isoformat() if self.data else None,
            'local': self.local,
            'tipo': self.tipo,
            'detento_id': self.detento_id
        }

class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) 
    role = db.Column(db.String(50), default='user') 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self): 
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

    def __repr__(self):
        return f'<User {self.username}>'
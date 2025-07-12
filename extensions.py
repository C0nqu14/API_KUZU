from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()

cors = CORS(supports_credentials=True)
login_manager = LoginManager()
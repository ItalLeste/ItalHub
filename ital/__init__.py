# É necessário manter este padrão de importação para evitar erros de circular imports.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__) # Instância do app.
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///italleste.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user}:{password}@{server}:{port}/{engine}"
app.config["SECRET_KEY"] = "a3190c71717b80582c2b580d8bc02528"

engine = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "home"

from ital import routes
from ital.models import QuadroFuncionarios

@login_manager.user_loader
def load_user(user_id):
    return QuadroFuncionarios.query.get(int(user_id))

if __name__ == "__main__":
    app.run()
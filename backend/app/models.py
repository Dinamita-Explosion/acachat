from . import db  # Importa el objeto 'db' desde __init__.py
import bcrypt  # Importa bcrypt para encriptar


class User(db.Model):
    # Define el nombre de la tabla
    __tablename__ = "users"

    # Definición de las columnas
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    region = db.Column(db.String(100), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Encripta la contraseña y la guarda."""
        # Genera el hash de la contraseña
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash."""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def __repr__(self):
        return f"<User {self.username}>"

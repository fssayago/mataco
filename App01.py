import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición de un modelo de prueba
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

# Crear las tablas en Neon (Solo para pruebas rápidas)
with app.app_context():
    db.create_all()

@app.route('/')
def test_db():
    try:
        # Intenta una consulta básica de prueba
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "Conexión exitosa a Neon Postgres"}), 200
    except Exception as e:
        return jsonify({"status": "Error de conexión", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
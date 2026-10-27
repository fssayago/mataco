import os
from flask import Flask, jsonify
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    # Conectarse a la base de datos de Neon usando la URL del .env
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route('/')
def index():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Crear una tabla de prueba si no existe
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visitas (
                id SERIAL PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # 2. Insertar un nuevo registro (una nueva visita)
        cur.execute('INSERT INTO visitas DEFAULT VALUES;')
        conn.commit()
        
        # 3. Consultar el total de registros
        cur.execute('SELECT COUNT(*) FROM visitas;')
        total_visitas = cur.fetchone()[0]
        
        cur.close()
        return jsonify({
            "status": "Conectado exitosamente a Neon DB!",
            "total_visitas_registradas": total_visitas
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # Ejecutar servidor local en modo desarrollo
    app.run(debug=True, port=5000)
    
import os
from flask import Flask
import psycopg

app = Flask(__name__)
DATABASE_URL = "postgresql://neondb_owner:npg_AQSmyrP64KJv@ep-mute-brook-b5p2x3tk.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

@app.route("/")
def home():
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT version();")
      version = cur.fetchone()[0]
  return f"Conectado a PostgreSQL en Neon: {version}"


if __name__ == "__main__":
  app.run(debug=True)
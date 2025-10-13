import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Docker Compose will set these environment variables for us.
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = "db"  # The service name from our docker-compose file

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")

@app.route('/')
def get_visits():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """))
        connection.execute(text("INSERT INTO visits (timestamp) VALUES (NOW());"))
        connection.commit()

        result = connection.execute(text("SELECT * FROM visits ORDER BY timestamp DESC;"))
        visits = [row._asdict() for row in result]
        return jsonify(visits)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from pathlib import Path
import mysql.connector
import os
from dotenv import load_dotenv

class Database:
    def execute(self, query):
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)

        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )

            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchone()[0]
                return rows

        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return None

        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def query(self, query):
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)

        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )

            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()[0]
                return rows

        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return None

        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()
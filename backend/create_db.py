import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Paramètres de connexion
DB_USER = "postgres"
DB_PASSWORD = "root"  # ⚠️ CHANGEZ ICI
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "feelback_db"

def create_database():
    try:
        # Se connecter à la base par défaut
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database="postgres"  # Base par défaut
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            # Créer la base de données
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"✅ Base de données '{DB_NAME}' créée avec succès !")
        else:
            print(f"ℹ️  La base de données '{DB_NAME}' existe déjà.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    create_database()
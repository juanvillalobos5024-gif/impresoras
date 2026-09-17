import os
import sys
sys.path.append('.')

# Load from .env BEFORE importing anything from app
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('POSTGRES_URL='):
                url = line.strip().split('=', 1)[1].strip('"')
                os.environ['POSTGRES_URL'] = url
                break

from app.database.db import init_db

print("Inicializando base de datos en Vercel Postgres...")
init_db()
print("¡Inicialización completada!")

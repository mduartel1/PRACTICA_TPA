import sys
from pathlib import Path

# Añadir la raíz del proyecto al sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Inicializar la base de datos una vez para los tests
try:
    from src.storage.database import init_db

    init_db()
except Exception:

    pass
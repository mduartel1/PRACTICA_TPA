import logging
from pathlib import Path

LOG_PATH = Path("logs/gestor.log")
LOG_PATH.parent.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("gestor")

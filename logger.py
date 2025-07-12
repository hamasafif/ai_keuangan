import os
import logging
from dotenv import load_dotenv

# Load variabel environment
load_dotenv()
DEBUG = os.getenv("DEBUG", "False") == "True"

# Emoji untuk setiap level log
EMOJI_LEVELS = {
    "DEBUG": "🔧",
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "🔥",
}

# Custom formatter untuk menambahkan emoji
class EmojiFormatter(logging.Formatter):
    def format(self, record):
        emoji = EMOJI_LEVELS.get(record.levelname, "")
        base = super().format(record)
        return f"{emoji} {base}"

# Inisialisasi logger hanya sekali
logger = logging.getLogger("KeuanganBot")

if not logger.handlers:
    formatter = EmojiFormatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Level log berdasarkan mode debug
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    logger.propagate = False  # Cegah duplikasi log di root logger

def get_logger():
    return logger

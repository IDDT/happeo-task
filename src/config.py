import os
import sys
import logging


# Logging.
logging.basicConfig(
    format='%(levelname)s:     %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout,
    force=True
)


# Paths.
TEMP_DIR = 'temp'
MODEL_PATH = os.path.join(TEMP_DIR, 'model.gguf')
DATABASE_PATH = os.path.join(TEMP_DIR, 'database.db')

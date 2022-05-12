import os
import tempfile
from pathlib import Path

# Persistent cache
MAGNA_DIR = os.path.join(Path.home(), '.magna')

# Temporary cache
CACHE_DIR = os.path.join(tempfile.gettempdir(), 'magna')

# Redis information
REDIS_HOST = os.environ.get('MAGNA_REDIS_HOST')
REDIS_PASS = os.environ.get('MAGNA_REDIS_PASS')
RQ_GENERAL = os.environ.get('MAGNA_RQ_GENERAL', 'general')

# Conda information
CONDA_PATH = os.environ.get('MAGNA_CONDA_PATH')

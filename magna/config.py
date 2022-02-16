import os
import tempfile
from pathlib import Path

# Persistent cache
MAGNA_DIR = os.path.join(Path.home(), '.magna')

# Temporary cache
CACHE_DIR = os.path.join(tempfile.gettempdir(), 'magna')

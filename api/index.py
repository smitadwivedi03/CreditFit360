import sys
import os

# Add parent directory to sys.path so app, ai_engine, and db are found by Python
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app

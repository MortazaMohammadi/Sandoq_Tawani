# -*- coding: utf-8 -*-
"""Database module initialization - re-export root db functions"""

import sys
import os

# Add parent directory to path to import root db.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from root db.py
import importlib.util
spec = importlib.util.spec_from_file_location("root_db", 
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db.py"))
root_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_db)

# Re-export functions
fetch_all = root_db.fetch_all
execute = root_db.execute
get_conn = root_db.get_conn

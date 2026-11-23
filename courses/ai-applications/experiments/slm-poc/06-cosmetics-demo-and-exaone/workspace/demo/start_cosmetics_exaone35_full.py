"""Experimental all-EXAONE skin controller; see saved7/34 before using."""
import os
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ['SKIN_CHAT_ENGINE']='exaone35'
os.environ.setdefault('COSMETICS_CHAT_PORT','18783')
runpy.run_module('demo.cosmetics_chat_server',run_name='__main__')

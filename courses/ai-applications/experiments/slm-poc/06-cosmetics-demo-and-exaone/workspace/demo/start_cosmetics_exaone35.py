"""Opt-in skin chat: trained SLM decisions, local EXAONE 3.5 replies; no API key."""
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ['SKIN_CHAT_ENGINE'] = 'domain'
os.environ['SKIN_CHAT_REPLY_BACKEND'] = 'exaone35'
os.environ['SKIN_CHAT_REPLY'] = 'on'
os.environ.setdefault('COSMETICS_CHAT_PORT', '18782')
runpy.run_module('demo.cosmetics_chat_server', run_name='__main__')

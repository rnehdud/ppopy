"""Local-only Poppy KB preview. No production route or external client."""
from .engine import PreviewEngine, load_kb
__all__ = ['PreviewEngine', 'load_kb']

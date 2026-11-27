"""Public SLM prompt, transport and fallback interfaces."""

from .openai_compat_client import OpenAICompatSLMClient
from .prompt_builder import (
    SYSTEM_PROMPT_NLU,
    SYSTEM_PROMPT_SOLUTION_HOLD,
    build_messages,
    build_nlu_messages,
)
from .rule_fallback import RuleBaselineFallback

__all__ = [
    "OpenAICompatSLMClient",
    "RuleBaselineFallback",
    "SYSTEM_PROMPT_NLU",
    "SYSTEM_PROMPT_SOLUTION_HOLD",
    "build_messages",
    "build_nlu_messages",
]

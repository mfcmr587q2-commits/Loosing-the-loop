"""LLM adapters for grounded reasoning.

The adapter is deliberately isolated from the safety kernel. The model proposes a
structured claim; it cannot authorize or execute an action.

The default configuration targets the large Qwen3 235B MoE model through any
OpenAI-compatible endpoint (for example vLLM or DashScope). Runtime details are
provided by environment variables so the same code can use a local GPU server or
a hosted API without changing the safety kernel.
"""
from __future__ import annotations

import json
import os
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # optional dependency
    OpenAI = None


SYSTEM_PROMPT = """You are the grounded reasoning component of Losing-the-Loop.
You are NOT the source of truth, validator, or authorization authority.
Use only supplied evidence and provenance. Never invent missing evidence.
Return JSON with: hypothesis, facts_used, assumptions, uncertainties,
counterevidence_needed, validation_plan, proposed_action.
If evidence conflicts or provenance is incomplete, say so explicitly.
"""

DEFAULT_QWEN_MODEL = os.getenv(
    "LLM_MODEL",
    "Qwen/Qwen3-235B-A22B-Instruct-2507",
)
DEFAULT_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:8000/v1")


class LocalLLMReasoner:
    """OpenAI-compatible reasoner adapter.

    Despite the historical class name, this works with local or hosted endpoints.
    The endpoint, API key, and model are supplied independently of the safety core.
    """

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
    ):
        if OpenAI is None:
            raise RuntimeError("Install optional dependency: pip install openai")
        self.base_url = base_url or DEFAULT_BASE_URL
        self.model = model or DEFAULT_QWEN_MODEL
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=api_key or os.getenv("LLM_API_KEY", "local"),
        )

    def reason(self, grounded_state: dict[str, Any]) -> dict[str, Any]:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(grounded_state)},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("LLM returned an empty response")
        return json.loads(content)

"""LLM adapter for grounded reasoning.

The adapter is deliberately isolated from the safety kernel. The model proposes a
structured claim; it cannot authorize or execute an action.
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


class LocalLLMReasoner:
    def __init__(self, base_url: str = "http://localhost:11434/v1", model: str = "llama3.2"):
        if OpenAI is None:
            raise RuntimeError("Install optional dependency: pip install openai")
        self.client = OpenAI(base_url=base_url, api_key=os.getenv("LLM_API_KEY", "local"))
        self.model = model

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
        return json.loads(response.choices[0].message.content)

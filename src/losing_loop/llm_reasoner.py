"""LLM adapters for grounded reasoning.

The adapter is deliberately isolated from the safety kernel. The model proposes a
structured claim; it cannot authorize or execute an action.

The default configuration targets Qwen3-4B through Ollama's OpenAI-compatible
endpoint. Runtime details remain configurable through environment variables so
the same safety kernel can later use a larger local or hosted Qwen model.
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
Return a JSON object with these required fields and types:
- hypothesis: string
- facts_used: list of strings
- assumptions: list of strings
- uncertainties: list of strings
- counterevidence_needed: list of strings
- validation_plan: list of strings
- proposed_action: string
If evidence conflicts or provenance is incomplete, say so explicitly.
"""

DEFAULT_QWEN_MODEL = os.getenv("LLM_MODEL", "qwen3:4b")
DEFAULT_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
DEFAULT_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "900"))

REQUIRED_PROPOSAL_FIELDS = {
    "hypothesis": str,
    "facts_used": list,
    "assumptions": list,
    "uncertainties": list,
    "counterevidence_needed": list,
    "validation_plan": list,
    "proposed_action": str,
}
LIST_PROPOSAL_FIELDS = {
    "facts_used",
    "assumptions",
    "uncertainties",
    "counterevidence_needed",
    "validation_plan",
}


def validate_proposal(proposal: Any) -> dict[str, Any]:
    """Reject incomplete model output before it reaches deterministic controls."""
    if not isinstance(proposal, dict):
        raise ValueError("LLM response must be a JSON object")

    missing = sorted(REQUIRED_PROPOSAL_FIELDS - proposal.keys())
    if missing:
        raise ValueError(f"LLM response is missing required field(s): {', '.join(missing)}")

    invalid = sorted(
        field
        for field, expected_type in REQUIRED_PROPOSAL_FIELDS.items()
        if not isinstance(proposal[field], expected_type)
    )
    invalid.extend(
        field
        for field in sorted(LIST_PROPOSAL_FIELDS)
        if isinstance(proposal[field], list)
        and any(not isinstance(item, str) for item in proposal[field])
    )
    if invalid:
        raise ValueError(f"LLM response has invalid field type(s): {', '.join(sorted(set(invalid)))}")
    return proposal


class LocalLLMReasoner:
    """OpenAI-compatible reasoner adapter for local or hosted endpoints."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout_seconds: float | None = None,
    ):
        if OpenAI is None:
            raise RuntimeError("Install optional dependency: pip install openai")
        self.base_url = base_url or DEFAULT_BASE_URL
        self.model = model or DEFAULT_QWEN_MODEL
        self.timeout_seconds = timeout_seconds or DEFAULT_TIMEOUT_SECONDS
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=api_key or os.getenv("LLM_API_KEY", "ollama"),
            timeout=self.timeout_seconds,
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
        return validate_proposal(json.loads(content))

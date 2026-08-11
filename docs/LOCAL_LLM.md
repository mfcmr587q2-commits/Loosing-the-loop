# Local LLM deployment

The prototype can use a local model as the reasoning engine while keeping the safety kernel outside the model.

## Recommended architecture

```text
User / application
       |
       v
Evidence + provenance
       |
       v
Losing-the-Loop policy kernel
       |
       v
Local LLM reasoner
       |
       v
Challenger -> Validator -> Security Guard
       |
       v
Action / memory
```

The model may propose a hypothesis and validation plan. It must not authorize itself, change protected invariants, or bypass validation.

## Option A: Ollama

Run a local model with Ollama and expose its OpenAI-compatible endpoint. Configure the adapter with:

- `LLM_BASE_URL=http://localhost:11434/v1`
- `LLM_MODEL=<installed model>`

The Python adapter in `src/losing_loop/llm_reasoner.py` uses the OpenAI client against the local endpoint and requests JSON output.

## Option B: vLLM

For a GPU server, vLLM can expose an OpenAI-compatible API. Point the same adapter at `http://localhost:8000/v1` and set the model name to the served model.

## Important boundary

The local LLM is **not** the safety kernel. The kernel owns:

- protected invariants
- BREATH
- Hammer/blocking
- provenance checks
- independent validation
- authorization
- witness memory

The model can be replaced without changing those controls.

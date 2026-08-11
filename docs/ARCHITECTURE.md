# Losing-the-Loop Grounded Reasoning System

This document defines the executable research architecture inspired by the semantic-grounding pattern in arXiv:2605.15097.

## Pipeline

Observation -> Evidence -> Provenance -> Grounded State -> Reasoning -> Counterevidence -> BREATH -> Validation -> Authorization -> Action -> New Observation

## Separation of powers

- Evidence is constructed independently of the model.
- The model produces hypotheses, not truth.
- Provenance must be traceable.
- Counterevidence must be preserved.
- Validation is independent of claim generation.
- Authorization is independent of reasoning.
- Protected invariants are enforced outside the model.

## Research status

This is a prototype specification. Thresholds and safety properties are hypotheses to be tested, not claims of guaranteed safety.

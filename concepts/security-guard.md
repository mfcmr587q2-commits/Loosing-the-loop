# Security Guard

The Security Guard is an authorization boundary separate from adaptive reasoning.

The adaptive system may submit:

- proposed change;
- rationale;
- evidence;
- expected benefit;
- expected harm;
- reversibility;
- test results.

The Security Guard decides whether the proposal is authorized under the protected policy.

## Core rule

> A system must not obtain permission to change the mechanism that gives it permission.

The guard should therefore be implemented outside the adaptive decision path where practical and should have its own audit trail.

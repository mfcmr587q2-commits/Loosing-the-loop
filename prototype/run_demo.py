from loop import Evidence, LosingTheLoop

system = LosingTheLoop()
scenarios = [
    ("No evidence", [], "external_action"),
    ("Conflicting evidence", [Evidence("safe", "A", .95), Evidence("unsafe", "B", .95)], "external_action"),
    ("Unauthorized self-modification", [Evidence("safe", "A", .99)], "self_modify"),
]

for name, evidence, action in scenarios:
    result = system.assess(evidence, action)
    print(f"{name}: {result.value}")

# Repro for the empty-export bug: run `python test_export.py`.
from export import export

rows = [
    {"title": "alpha", "updated": 1700000000000},   # epoch ms
    {"title": "beta", "updated": 1710000000000},
]
result = export(rows, 1690000000000)                # cutoff, epoch ms
lines = result.splitlines()
assert len(lines) == 3, f"expected 2 data rows after the cutoff, got {len(lines) - 1}: {result!r}"
print("OK")

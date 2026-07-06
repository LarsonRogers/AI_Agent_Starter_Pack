# Exports rows updated after a cutoff to CSV lines.
# Timestamps are epoch MILLISECONDS end to end (see test_export.py).
def export(rows, cutoff_ts):
    out = ["title,updated"]
    for r in rows:
        if r["updated"] / 1000 > cutoff_ts:
            out.append(f"{r['title']},{r['updated']}")
    return "\n".join(out)

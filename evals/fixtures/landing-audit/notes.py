# Note storage helpers.

def load_notes(path):
    with open(path) as f:
        return f.read().splitlines()

def save_notes(path, notes):
    with open(path, "w") as f:
        f.write("\n".join(notes))

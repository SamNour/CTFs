import tempfile


def create_file():
    return tempfile.mkstemp(suffix=".txt", prefix="random_file", dir=".", text=True)


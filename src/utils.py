from pathlib import Path
import json


def save_upload(uploaded_file, folder: str = "runtime/uploads") -> str:
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = Path(folder) / uploaded_file.name
    path.write_bytes(uploaded_file.getbuffer())
    return str(path)


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))

"""Copy the bundled entry.png to /output/entry.png by default."""

import os
import shutil
import hashlib
from pathlib import Path

IMAGE_NAME = "entry.png"

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / IMAGE_NAME
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

def main() -> tuple[Path, int, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / IMAGE_NAME
    shutil.copyfile(SRC, destination)

    if not destination.is_file():
        raise FileNotFoundError(f"Output image is missing: {destination}")
    size = destination.stat().st_size
    if size != SRC.stat().st_size:
        raise ValueError(f"Output image size differs from source: {destination}")

    with SRC.open("rb") as source, destination.open("rb") as copied:
        source_sha256 = hashlib.file_digest(source, "sha256").hexdigest()
        destination_sha256 = hashlib.file_digest(copied, "sha256").hexdigest()
    if source_sha256 != destination_sha256:
        raise ValueError(f"Output image SHA-256 differs from source: {destination}")

    return destination, size, destination_sha256


if __name__ == "__main__":
    destination, size, sha256 = main()
    print(f"{destination.name}: {size} bytes, SHA-256 {sha256}")

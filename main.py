"""Copy the prepared front-page image (assets/entry.png) to the output folder."""
import os
import shutil
import struct
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets", "entry.png")


def main():
    with open(SRC, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("assets/entry.png is not a PNG")
    w, h = struct.unpack(">II", head[16:24])
    size = os.path.getsize(SRC)
    if w > 1024 or h > 1024 or size > 1048576:
        sys.exit(f"entry too large: {w}x{h}, {size} bytes")
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out, "entry.png"))
    print(f"wrote {out}/entry.png ({w}x{h}, {size} bytes)")


if __name__ == "__main__":
    main()

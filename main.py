#!/usr/bin/env python3
"""Entry for make.fun's "Sum up 25 November's world news in one image" bounty.

The picture itself was drawn programmatically by draw_entry.py (kept beside
this file): a 1024x1024 front-page-style summary of Wednesday 25 November
2026 — Shenzhou-24 flying Pakistan's first astronaut to China's space
station, four tankers struck in the Strait of Hormuz, the Houthi strike on
Riyadh's tower, new US tariffs and the Wall Street slide, Huawei's US
conviction, and Ukraine's energy strikes amid peace talks.

This program runs with no network, so it simply installs the picture it
ships with as /output/entry.png and verifies the bytes it wrote.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = "/output" if os.path.isdir("/output") or os.access("/", os.W_OK) else os.path.join(HERE, "output")
TARGET = os.path.join(OUT_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # the bounty caps the image at 1 MiB


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"entry image missing: {SOURCE}", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    with open(TARGET, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
    size = os.path.getsize(TARGET)
    if head != PNG_MAGIC:
        print("written file is not a PNG", file=sys.stderr)
        return 1
    if size > MAX_BYTES:
        print(f"image too large: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote {TARGET} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

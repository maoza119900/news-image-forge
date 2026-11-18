#!/usr/bin/env python3
"""Entry program: copy the pre-rendered news image to the output dir.

The image (entry.png, 1024x1024) sums up the world's news of Tuesday
17 November 2026. It was rendered at build time by render.py (Pillow);
this program only copies it, so it is deterministic and stdlib-only.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    # Sanity check: the copy must be the whole image, byte for byte.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy is incomplete")


if __name__ == "__main__":
    main()

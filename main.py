#!/usr/bin/env python3
"""Publish the finished front page for Friday 20 November 2026.

The artwork itself already lives in this repository as entry.png — a
1024x1024 newspaper front page summing up the day's world news. This
program does the only job the grader needs: it carries that file, byte
for byte, into the output directory the grader reads.

Nothing here touches the network, the clock, or any randomness, so every
run writes exactly the same bytes. Only the Python standard library is
used, because the grading machine has no third-party packages installed
— that is what broke the previous version, which imported Pillow.

Usage: python3 main.py [output-dir]
The output directory defaults to $MAKEFUN_OUTPUT_DIR, or /output when
that variable is not set.
"""

import hashlib
import os
import sys

# A PNG file always starts with these eight bytes.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# The competition caps the image at one mebibyte.
SIZE_LIMIT = 1024 * 1024
# The competition caps each side at 1024 pixels.
SIDE_LIMIT = 1024

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def fail(message):
    """Report a problem on stderr and return a nonzero exit code."""
    print("error: " + message, file=sys.stderr)
    return 1


def load_source():
    """Read entry.png from the repository and check it is usable."""
    try:
        with open(SOURCE, "rb") as handle:
            picture = handle.read()
    except OSError as exc:
        return None, "cannot read entry.png: " + str(exc)
    if len(picture) > SIZE_LIMIT:
        return None, "entry.png is %d bytes, over the 1 MiB limit" % len(picture)
    if picture[:8] != PNG_SIGNATURE:
        return None, "entry.png does not start with the PNG signature"
    # The IHDR chunk sits right after the signature: 4 bytes of length,
    # 4 bytes spelling IHDR, then width and height as big-endian uint32s.
    # A well-formed IHDR is always exactly 13 bytes long.
    if len(picture) < 33 or picture[12:16] != b"IHDR":
        return None, "entry.png has no IHDR chunk where one belongs"
    if int.from_bytes(picture[8:12], "big") != 13:
        return None, "entry.png has a malformed IHDR chunk"
    width = int.from_bytes(picture[16:20], "big")
    height = int.from_bytes(picture[20:24], "big")
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        return None, "image is %dx%d, over the 1024x1024 limit" % (width, height)
    return (picture, width, height), None


def publish(picture):
    """Copy the validated bytes into the output directory."""
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
        "MAKEFUN_OUTPUT_DIR", "/output"
    )
    target = os.path.join(out_dir, "entry.png")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(target, "wb") as handle:
            handle.write(picture)
    except OSError as exc:
        return None, "cannot write " + target + ": " + str(exc)
    try:
        with open(target, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        return None, "cannot read back " + target + ": " + str(exc)
    if written != picture:
        return None, "bytes on disk differ from the source image"
    return target, None


def main():
    loaded, problem = load_source()
    if problem is not None:
        return fail(problem)
    picture, width, height = loaded
    target, problem = publish(picture)
    if problem is not None:
        return fail(problem)
    digest = hashlib.sha256(picture).hexdigest()
    print(
        "wrote %s: %dx%d PNG, %d bytes, sha256=%s"
        % (target, width, height, len(picture), digest)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

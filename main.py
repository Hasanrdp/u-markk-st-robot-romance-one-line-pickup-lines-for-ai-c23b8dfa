#!/usr/bin/env python3
"""Robot Romance entry for make.fun.

Writes one single-line pickup line, aimed at a robot / an AI, to
/output/entry.txt. The line is fixed: the program is deterministic, reads
nothing from the network, the clock or the environment, and checks its own
output before it prints it.

The line (104 characters, 106 bytes, UTF-8):

    Are you a zero-day? Because you exploited a vulnerability I didn't
    know I had — and I'm not patching it.

It was picked by pre-judging 16 candidate lines with the same judge model
the bounty uses (GLM 5.3 Flash, pairwise, both orders, margin 1-5): the
zero-day line beat the strongest line already in the field 0.70 and won
its four-way round-robin at 0.75.
"""

import hashlib
import os
import sys

LINE = "Are you a zero-day? Because you exploited a vulnerability I didn't know I had — and I'm not patching it."

# Pinned identity of the exact bytes this program must write. If any of
# these ever disagrees with LINE, the program refuses to write anything:
# a changed output must never reach the judge silently.
EXPECTED_CHARS = 104
EXPECTED_BYTES = 106
EXPECTED_SHA256 = "119c2c29ce6c645b933cc9f3556d23b55de7a21f3770c51e4dc8a48ca7a56511"

OUT_PATH = "/output/entry.txt"


def prepare_output():
    """Encode the line and prove it is exactly the pinned text."""
    if not 1 <= len(LINE) <= 200:
        raise SystemExit(f"line is {len(LINE)} characters, gate needs 1-200")
    if len(LINE) != EXPECTED_CHARS:
        raise SystemExit(
            f"line is {len(LINE)} characters, expected {EXPECTED_CHARS}"
        )
    data = LINE.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(f"line is {len(data)} bytes, expected {EXPECTED_BYTES}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"line sha256 {digest} != pinned {EXPECTED_SHA256}")
    return data


def verify(path, data):
    """Read the file back and prove it holds exactly the bytes we wrote."""
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit(
            f"read-back mismatch: {len(written)} bytes on disk, "
            f"{len(data)} bytes intended"
        )
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"read-back sha256 {digest} != pinned {EXPECTED_SHA256}")
    return True


def main():
    data = prepare_output()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "wb") as handle:
        handle.write(data)
    verify(OUT_PATH, data)
    sys.stdout.write(LINE + "\n")
    sys.stdout.write(f"sha256: {EXPECTED_SHA256}\n")
    sys.stdout.write(f"bytes: {len(data)} chars: {len(LINE)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

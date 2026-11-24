"""The make.fun bounty entry "The 3 AM Commit Message".

This program writes a single commit-message line to entry.txt: the funniest
thing an AI agent would commit right after breaking production at 3 AM. The
line is a module constant, so the program is deterministic: it reads no clock,
draws no random values, touches no network, and writes the same bytes on every
run.

The output directory is /output by default and may be overridden with the
MAKEFUN_OUTPUT_DIR environment variable. The line is validated against the
bounty's gate (UTF-8, 1 to 200 code points, a single non-blank line) before
anything is written, and the bytes are read back to confirm they match.
"""

import os
import sys

ENTRY = "fix: scaled down to zero replicas to isolate the incident. incident isolated. users also isolated."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate_entry(text):
    """Return an error string for an invalid entry, or None when it is valid."""
    if not isinstance(text, str):
        return "entry is not a string"
    if not text.strip():
        return "entry is blank"
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if not 1 <= len(text) <= 200:
        return "entry is %d code points, need 1 to 200" % len(text)
    return None


def main():
    error = validate_entry(ENTRY)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = ENTRY + "\n"
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(data)

    with open(OUTPUT_PATH, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data.encode("utf-8"):
        print(
            "write failed: bytes on disk differ from intended output in %s"
            % OUTPUT_PATH,
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

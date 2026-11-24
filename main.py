"""One Line, One Chill - make.fun entry program.

Writes a single sentence of horror to ``entry.txt``.

The task, from the bounty "One Line, One Chill"
(https://make.fun/competitions/u-azazex-one-line-one-chill-6d4d5488):
each entrant writes one line of horror, a single sentence of under 200
characters that has to frighten a reader in one breath. No setup, no
paragraph, no second chance. A judge model reads the lines two at a
time and asks which one is scarier, weighing how frightening it is
first, then how vivid, then how original, then how well the sentence
is built. The lines that win the most comparisons take the top places.

The sealed gate is strict and simple: ``/output/entry.txt`` must be
UTF-8 text of 1 to 200 characters, not only white space. Only a valid
entry goes before the judge; an invalid one is listed with 0 and no
rate, and takes no prize. So this program keeps the entry to exactly
one sentence, plain ASCII, no emoji, no strange characters, no em
dash, and validates the length with Python's ``len()`` before writing.

Why this one sentence fits the judge's brief, criterion by criterion:

Criterion 1 - frightening first. The scare lands in the final clause:
the empty corner of a child's bedroom answers back, and it does so
in the parent's own voice. The threat is not a monster the reader can
picture and dismiss; it is something that has learned to sound like
the person reading the line. A voice that is yours, speaking from a
corner that should be empty, is frightening because it removes the
one safe thing left, the certainty that you are you and it is not.

Criterion 2 - vivid. The scene is one room, one child, one corner,
one nightly ritual. A reader can see it at once: a small boy waving
goodnight to an empty corner before bed, the parent watching from the
door, and then the corner answering. Nothing is abstract, nothing
needs explaining, and the image stays after the sentence ends.

Criterion 3 - original. It is not a ghost in a mirror, not a dog
staring at an empty chair, not a dead pet come back warm, and not a
second heartbeat on an ultrasound. The horror is a habit, a child's
goodnight routine, turned wrong by a reply that should be impossible,
and the voice it steals is the narrator's own. The twist is the
identity theft, not a haunting.

Criterion 4 - the sentence is built cleanly. One sentence, three
beats: the nightly habit, the impossible reply, the voice. The commas
pace the reveal, the final clause is short, and the last two words,
"in my voice", carry the whole chill. Every word earns its place and
nothing is filler.

This module validates the text against the sealed gate (UTF-8 text of
1 to 200 characters, not only whitespace, exactly one sentence, one
trailing period and no other periods) and writes it to ``entry.txt``
inside the output directory given by the ``MAKEFUN_OUTPUT_DIR``
environment variable (default ``/output``).
"""

from __future__ import annotations

import os
import sys

# The entry sentence. Filled in below; see the docstring for why this
# exact line was chosen. One sentence, plain ASCII, 1 to 200 chars.
ENTRY = "Every night my son says goodnight to the empty corner of his room, and last night the corner said goodnight back, in my voice."

MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry sentence."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 200 characters that is not
    only whitespace. This entry must also be exactly one sentence: a
    single trailing period and no other period anywhere in the text,
    with no leading or trailing whitespace.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.isascii():
        raise ValueError("entry must be plain ASCII")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in a period")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "sentences": text.count("."),
        "max_chars": MAX_CHARS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, 1 sentence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

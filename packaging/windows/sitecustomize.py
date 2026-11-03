"""Use UTF-8 for every interpreter in Cloudra's isolated Windows runtime."""

import sys

for stream in (sys.stdin, sys.stdout, sys.stderr):
    if stream is not None:
        stream.reconfigure(encoding="utf-8")

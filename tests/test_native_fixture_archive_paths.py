"""Historical fixtures must extract on Windows without changing native bytes."""

import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath

FIXTURES = Path(__file__).parent / "fixtures" / "native_endpoint_lineage_20261020"
_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)
}


def _archive_records(value):
    if isinstance(value, dict):
        if "archive" in value:
            yield value
        for child in value.values():
            yield from _archive_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from _archive_records(child)


def test_native_fixture_archives_extract_on_windows_and_preserve_source_hashes():
    manifest = json.loads((FIXTURES / "manifest.json").read_text())
    records = list(_archive_records(manifest))
    assert records
    for record in records:
        relative = record["archive"]
        for part in PurePosixPath(relative).parts:
            assert part.split(".", 1)[0].upper() not in _RESERVED_NAMES, relative
        archive = (FIXTURES / relative).read_bytes()
        if "gzip_sha256" in record:
            assert hashlib.sha256(archive).hexdigest() == record["gzip_sha256"], relative
        source = gzip.decompress(archive) if relative.endswith(".gz") else archive
        assert hashlib.sha256(source).hexdigest() == record["sha256"], relative

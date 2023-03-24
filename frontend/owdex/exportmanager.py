import tarfile
from io import BytesIO
from hashlib import file_digest as digest
from pathlib import Path

from flask import current_app as app

import jsonlines


def entries_to_record(entries):
    with BytesIO() as buffer:
        with jsonlines.Writer(buffer) as writer:
            writer.write_all([
                app.lm.filter_entry(entry, ("url", "title", "submitter"))
                for entry in entries
            ])

        filename = f"{digest(buffer, 'md5').hexdigest()}.jsonl"

        path = Path(f"/tmp/exports/")
        path.mkdir(parents=True, exist_ok=True)
        (path / filename).write_bytes(buffer.getbuffer())

    return filename

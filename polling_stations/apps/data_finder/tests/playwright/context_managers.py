from contextlib import contextmanager

import pytest


@contextmanager
def check_for_console_errors(page_context):
    errors = []
    page_context.on(
        "console", lambda msg: errors.append(msg.text) if msg.type == "error" else None
    )
    yield
    if len(errors) != 0:
        pytest.fail(f"Console errors detected {errors}")

#!/usr/bin/env bash
set -xeE

UV_CONSTRAINT=">=0.4.27,<0.5.0"

if [ "$CI" = "true" ]; then
    pip install uv"$UV_CONSTRAINT"
elif [ -v LAMBDA_TASK_ROOT ]; then
    python -m venv /tmp/uv_venv
    source /tmp/uv_venv/bin/activate
    pip install uv"$UV_CONSTRAINT"
else
    sudo PIP_BREAK_SYSTEM_PACKAGES=1 pip install uv"$UV_CONSTRAINT"
fi

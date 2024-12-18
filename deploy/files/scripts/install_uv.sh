#!/usr/bin/env bash
set -xeE

UV_CONSTRAINT=">=0.4.27,<0.5.0"

if [ "$CI" = "true" ]; then
    pip install uv"$UV_CONSTRAINT"
else
    sudo PIP_BREAK_SYSTEM_PACKAGES=1 pip install uv"$UV_CONSTRAINT"
fi

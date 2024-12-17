#!/bin/bash
set -euxo pipefail

uv sync --all-packages --group testing --group dev

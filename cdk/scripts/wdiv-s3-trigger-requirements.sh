#!/bin/bash
set -euxo pipefail

PARENT_DIR="$(dirname "$(dirname "$0")")"

uv export --no-hashes --package wdiv-s3-trigger > "$PARENT_DIR/lambdas/wdiv-s3-trigger/requirements.txt"

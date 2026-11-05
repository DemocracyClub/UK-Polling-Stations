#!/bin/bash
set -euxo pipefail

PARENT_DIR="$(dirname "$(dirname "$0")")"

uv export --no-hashes --package format-ssm-command-event > "$PARENT_DIR/lambdas/format_ssm_command_event/requirements.txt"

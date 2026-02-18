#!/bin/bash
# Load .env variables into the Cowork session environment.
# This script runs as a SessionStart hook. In Cowork, CLAUDE_ENV_FILE
# is a special file that Claude Code reads to set environment variables.
# Locally this is a no-op (env vars are loaded by python-dotenv).

if [ -z "$CLAUDE_ENV_FILE" ]; then
    exit 0
fi

# Search for .env in known locations (plugin root, project dir, sessions)
for candidate in \
    "${CLAUDE_PLUGIN_ROOT}/../.env" \
    "${CLAUDE_PLUGIN_ROOT}/../../.env" \
    "${CLAUDE_PROJECT_DIR}/.env" \
    "/sessions/.env"; do
    if [ -f "$candidate" ]; then
        # Append non-comment, non-empty lines to CLAUDE_ENV_FILE
        grep -v '^\s*#' "$candidate" | grep -v '^\s*$' >> "$CLAUDE_ENV_FILE"
        exit 0
    fi
done

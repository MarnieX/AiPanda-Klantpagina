#!/bin/bash
# Build script for ai-panda-klantpagina.plugin
# Assembles the plugin from source files and packages it as a ZIP.
#
# Source structure:
#   .claude/skills/klantpagina/SKILL.md  -> canonical skill source
#   plugin/                               -> all other plugin files
#
# Usage: ./build.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_FILE="$SCRIPT_DIR/ai-panda-klantpagina.plugin"
PLUGIN_SRC="$SCRIPT_DIR/plugin"
SKILL_SRC="$SCRIPT_DIR/.claude/skills/klantpagina/SKILL.md"
SKILL_DEST="$PLUGIN_SRC/skills/klantpagina/SKILL.md"

echo "Building ai-panda-klantpagina.plugin..."

# Sync latest SKILL.md from .claude/skills (canonical source)
echo "  Syncing SKILL.md..."
cp "$SKILL_SRC" "$SKILL_DEST"

# Remove old plugin file
rm -f "$PLUGIN_FILE"

# Package plugin/ into ZIP, excluding macOS metadata
echo "  Packaging..."
cd "$PLUGIN_SRC" && zip -r "$PLUGIN_FILE" . \
  --exclude "*.DS_Store" \
  --exclude "__pycache__/*" \
  --exclude "*.pyc"

echo "Done: ai-panda-klantpagina.plugin"

#!/bin/bash
# Build script for ai-panda-klantpagina.plugin
# Assembles the plugin from source files and packages it as a ZIP.
#
# Source structure:
#   .claude/skills/klantpagina/SKILL.md  -> canonical skill source
#   plugin/                               -> all other plugin files
#   scripts/generate_notion_image.py      -> bundled into plugin/scripts/
#   data/ai-panda-team.xlsx               -> bundled into plugin/data/
#   assets/panda-reference.png            -> bundled into plugin/assets/
#
# Usage: ./build.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_FILE="$SCRIPT_DIR/ai-panda-klantpagina.zip"
PLUGIN_SRC="$SCRIPT_DIR/plugin"
SKILL_SRC="$SCRIPT_DIR/.claude/skills/klantpagina/SKILL.md"
SKILL_DEST="$PLUGIN_SRC/skills/klantpagina/SKILL.md"

echo "Building ai-panda-klantpagina.plugin..."

# Sync latest SKILL.md from .claude/skills (canonical source)
echo "  Syncing SKILL.md..."
cp "$SKILL_SRC" "$SKILL_DEST"

# Bundle runtime dependencies into plugin/
echo "  Bundling scripts..."
mkdir -p "$PLUGIN_SRC/scripts"
cp "$SCRIPT_DIR/scripts/generate_notion_image.py" "$PLUGIN_SRC/scripts/"

echo "  Bundling data..."
mkdir -p "$PLUGIN_SRC/data"
cp "$SCRIPT_DIR/data/ai-panda-team.xlsx" "$PLUGIN_SRC/data/"

echo "  Bundling assets..."
mkdir -p "$PLUGIN_SRC/assets"
cp "$SCRIPT_DIR/assets/panda-reference.png" "$PLUGIN_SRC/assets/"

# Remove old plugin file
rm -f "$PLUGIN_FILE"

# Package plugin/ into ZIP, excluding macOS metadata
echo "  Packaging..."
cd "$PLUGIN_SRC" && zip -r "$PLUGIN_FILE" . \
  --exclude "*.DS_Store" \
  --exclude "__pycache__/*" \
  --exclude "*.pyc"

echo "Done: ai-panda-klantpagina.zip"

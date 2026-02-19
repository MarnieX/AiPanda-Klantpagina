#!/bin/bash
# Build script for ai-panda-klantpagina.plugin v2
# Assembles an isolated build at dist/plugin and packages it as a ZIP.
#
# Usage: ./build.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_FILE="$SCRIPT_DIR/ai-panda-klantpagina.zip"
PLUGIN_SRC="$SCRIPT_DIR/plugin"
BUILD_ROOT="$SCRIPT_DIR/dist"
BUILD_PLUGIN="$BUILD_ROOT/plugin"

echo "Building ai-panda-klantpagina.plugin v2..."

echo "  Preparing build workspace..."
rm -rf "$BUILD_PLUGIN"
mkdir -p "$BUILD_PLUGIN"
cp -R "$PLUGIN_SRC"/. "$BUILD_PLUGIN"/

# Never mutate source plugin folder; regenerate build content only in dist/plugin.
rm -rf "$BUILD_PLUGIN/skills" "$BUILD_PLUGIN/scripts" "$BUILD_PLUGIN/data" "$BUILD_PLUGIN/assets"
mkdir -p "$BUILD_PLUGIN/skills" "$BUILD_PLUGIN/scripts" "$BUILD_PLUGIN/data" "$BUILD_PLUGIN/assets"

echo "  Syncing v2 skills from .claude/skills..."
mkdir -p "$BUILD_PLUGIN/skills/klantpagina-v2"
cp "$SCRIPT_DIR/.claude/skills/klantpagina-v2/SKILL.md" "$BUILD_PLUGIN/skills/klantpagina-v2/SKILL.md"
mkdir -p "$BUILD_PLUGIN/skills/gemini-image-v2"
cp "$SCRIPT_DIR/.claude/skills/gemini-image-v2/SKILL.md" "$BUILD_PLUGIN/skills/gemini-image-v2/SKILL.md"
mkdir -p "$BUILD_PLUGIN/skills/ai-quiz-v2"
cp "$SCRIPT_DIR/.claude/skills/ai-quiz-v2/SKILL.md" "$BUILD_PLUGIN/skills/ai-quiz-v2/SKILL.md"
mkdir -p "$BUILD_PLUGIN/skills/ai-toekomstvisie-v2"
cp "$SCRIPT_DIR/.claude/skills/ai-toekomstvisie-v2/SKILL.md" "$BUILD_PLUGIN/skills/ai-toekomstvisie-v2/SKILL.md"

# V1 skills zijn gearchiveerd in .claude/skills/_archive/ en worden niet meegebundeld.

echo "  Bundling runtime files..."
cp "$SCRIPT_DIR/scripts/generate_notion_image.py" "$BUILD_PLUGIN/scripts/"
cp "$SCRIPT_DIR/data/ai-panda-team.xlsx" "$BUILD_PLUGIN/data/"
cp "$SCRIPT_DIR/assets/panda-reference.png" "$BUILD_PLUGIN/assets/"

# Remove deprecated files from build output if present.
rm -rf "$BUILD_PLUGIN/hooks"
rm -f "$BUILD_PLUGIN/servers/gemini-image-server.py"

echo "  Packaging..."
rm -f "$PLUGIN_FILE"
cd "$BUILD_PLUGIN" && zip -r "$PLUGIN_FILE" . \
  --exclude "*.DS_Store" \
  --exclude "*__pycache__*" \
  --exclude "*.pyc"

echo "Done: ai-panda-klantpagina.zip"

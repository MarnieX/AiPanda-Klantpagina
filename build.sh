#!/bin/bash
# Build script for ai-panda-klantpagina.plugin v2
# Assembles the plugin from source files and packages it as a ZIP.
#
# Source structure:
#   .claude/skills/klantpagina-v2/SKILL.md     -> canonical v2 skill source
#   .claude/skills/gemini-image-v2/SKILL.md    -> canonical v2 skill source
#   .claude/skills/ai-quiz-v2/SKILL.md         -> canonical v2 skill source
#   .claude/skills/ai-toekomstvisie-v2/SKILL.md -> canonical v2 skill source
#   plugin/                                     -> all other plugin files
#   plugin/templates/klantpagina.md            -> Notion page template
#   scripts/generate_notion_image.py           -> bundled into plugin/scripts/
#   data/ai-panda-team.xlsx                    -> bundled into plugin/data/
#   assets/panda-reference.png                 -> bundled into plugin/assets/
#
# Usage: ./build.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_FILE="$SCRIPT_DIR/ai-panda-klantpagina.zip"
PLUGIN_SRC="$SCRIPT_DIR/plugin"

echo "Building ai-panda-klantpagina.plugin v2..."

# Sync v2 skills from .claude/skills (canonical source)
echo "  Syncing klantpagina-v2 SKILL.md..."
mkdir -p "$PLUGIN_SRC/skills/klantpagina-v2"
cp "$SCRIPT_DIR/.claude/skills/klantpagina-v2/SKILL.md" "$PLUGIN_SRC/skills/klantpagina-v2/SKILL.md"

echo "  Syncing gemini-image-v2 SKILL.md..."
mkdir -p "$PLUGIN_SRC/skills/gemini-image-v2"
cp "$SCRIPT_DIR/.claude/skills/gemini-image-v2/SKILL.md" "$PLUGIN_SRC/skills/gemini-image-v2/SKILL.md"

echo "  Syncing ai-quiz-v2 SKILL.md..."
mkdir -p "$PLUGIN_SRC/skills/ai-quiz-v2"
cp "$SCRIPT_DIR/.claude/skills/ai-quiz-v2/SKILL.md" "$PLUGIN_SRC/skills/ai-quiz-v2/SKILL.md"

echo "  Syncing ai-toekomstvisie-v2 SKILL.md..."
mkdir -p "$PLUGIN_SRC/skills/ai-toekomstvisie-v2"
cp "$SCRIPT_DIR/.claude/skills/ai-toekomstvisie-v2/SKILL.md" "$PLUGIN_SRC/skills/ai-toekomstvisie-v2/SKILL.md"

# Also sync v1 skills (kept for backwards compatibility)
echo "  Syncing v1 skills..."
mkdir -p "$PLUGIN_SRC/skills/klantpagina"
cp "$SCRIPT_DIR/.claude/skills/klantpagina/SKILL.md" "$PLUGIN_SRC/skills/klantpagina/SKILL.md"

mkdir -p "$PLUGIN_SRC/skills/gemini-image"
cp "$SCRIPT_DIR/.claude/skills/gemini-image/SKILL.md" "$PLUGIN_SRC/skills/gemini-image/SKILL.md"

mkdir -p "$PLUGIN_SRC/skills/ai-toekomstvisie"
cp "$SCRIPT_DIR/.claude/skills/ai-toekomstvisie/SKILL.md" "$PLUGIN_SRC/skills/ai-toekomstvisie/SKILL.md"

if [ -d "$SCRIPT_DIR/.claude/skills/ai-quiz" ]; then
    mkdir -p "$PLUGIN_SRC/skills/ai-quiz"
    cp "$SCRIPT_DIR/.claude/skills/ai-quiz/SKILL.md" "$PLUGIN_SRC/skills/ai-quiz/SKILL.md"
fi

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

# Templates are already in plugin/templates/ (no sync needed)
echo "  Templates: OK (in-place)"

# Clean up old files that no longer exist
rm -rf "$PLUGIN_SRC/hooks"
rm -f "$PLUGIN_SRC/servers/gemini-image-server.py"

# Remove old plugin file
rm -f "$PLUGIN_FILE"

# Package plugin/ into ZIP, excluding macOS metadata
echo "  Packaging..."
cd "$PLUGIN_SRC" && zip -r "$PLUGIN_FILE" . \
  --exclude "*.DS_Store" \
  --exclude "*__pycache__*" \
  --exclude "*.pyc"

echo "Done: ai-panda-klantpagina.zip"

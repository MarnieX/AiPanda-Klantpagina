#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

IMAGE_GENERATION="FAIL"
NOTION_IMAGE_EMBED="FAIL"
OVERALL="NOT READY"

echo "=== Cowork Readiness Check ==="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo

if pytest -q tests/integration/test_cowork_image_notion_flow.py::test_image_generation_to_notion_payload_happy_path >/tmp/cowork_image_generation.log 2>&1; then
  IMAGE_GENERATION="PASS"
fi

if pytest -q tests/integration/test_cowork_image_notion_flow.py::test_image_failure_omits_hero_image_line >/tmp/cowork_notion_embed.log 2>&1; then
  NOTION_IMAGE_EMBED="PASS"
fi

if [[ "$IMAGE_GENERATION" == "PASS" && "$NOTION_IMAGE_EMBED" == "PASS" ]]; then
  OVERALL="READY"
fi

echo "IMAGE_GENERATION:  $IMAGE_GENERATION"
echo "NOTION_IMAGE_EMBED: $NOTION_IMAGE_EMBED"
echo "OVERALL: $OVERALL"
echo

if [[ "$OVERALL" != "READY" ]]; then
  echo "--- Debug (image generation test) ---"
  cat /tmp/cowork_image_generation.log || true
  echo
  echo "--- Debug (notion image embed test) ---"
  cat /tmp/cowork_notion_embed.log || true
  exit 1
fi


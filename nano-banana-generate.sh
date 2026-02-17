#!/bin/bash
# ============================================
# 🍌 Nano Banana Pro — One-Click Image Generator
# ============================================
# Dit script voert het laatst gegenereerde prompt-bestand uit,
# OF accepteert een directe beschrijving als argument.
#
# Gebruik:
#   ./nano-banana-generate.sh                          # Voert laatste prompt uit
#   ./nano-banana-generate.sh "een panda in een bos"   # Directe prompt
#   ./nano-banana-generate.sh --watch                  # Continu monitoren voor nieuwe prompts
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROMPT_DIR="$SCRIPT_DIR/prompts"
OUTPUT_DIR="$SCRIPT_DIR/generated"
ENV_FILE="$SCRIPT_DIR/.env"

# Kleuren
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Laad .env
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY niet gevonden in $ENV_FILE"
    exit 1
fi

# Maak directories
mkdir -p "$PROMPT_DIR" "$OUTPUT_DIR"

# Functie: genereer afbeelding
generate() {
    local prompt="$1"
    local model="${2:-gemini-2.0-flash-exp}"
    local ratio="${3:-1:1}"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local output_file="$OUTPUT_DIR/image_${timestamp}.png"

    echo -e "${BLUE}🍌 Nano Banana Pro — Generating...${NC}"
    echo -e "   Prompt:  ${prompt:0:80}..."
    echo -e "   Model:   $model"
    echo -e "   Output:  $output_file"
    echo ""

    python3 "$SCRIPT_DIR/generate_notion_image.py" \
        "$prompt" \
        --model "$model" \
        --ratio "$ratio" \
        --output "$output_file"

    if [ $? -eq 0 ] && [ -f "$output_file" ]; then
        echo ""
        echo -e "${GREEN}✅ Afbeelding gegenereerd!${NC}"
        echo -e "   📁 $output_file"

        # Open in Finder/Preview op macOS
        if command -v open &> /dev/null; then
            open "$output_file"
            echo -e "   👀 Geopend in Preview"
        fi
    else
        echo "❌ Generatie mislukt"
        exit 1
    fi
}

# Functie: watch mode — monitor prompts directory
watch_mode() {
    echo -e "${YELLOW}👀 Watch mode actief — monitoring $PROMPT_DIR voor nieuwe .txt bestanden${NC}"
    echo "   Druk Ctrl+C om te stoppen"
    echo ""

    # Markeer bestaande bestanden als verwerkt
    local processed_file="$PROMPT_DIR/.processed"
    touch "$processed_file"

    while true; do
        for prompt_file in "$PROMPT_DIR"/*.txt; do
            [ -f "$prompt_file" ] || continue

            # Skip als al verwerkt (ouder dan marker)
            if [ "$prompt_file" -ot "$processed_file" ]; then
                continue
            fi

            echo -e "${BLUE}📨 Nieuw prompt gevonden: $(basename "$prompt_file")${NC}"

            # Lees prompt en optionele metadata
            local prompt=$(head -1 "$prompt_file")
            local model=$(grep "^model:" "$prompt_file" | cut -d: -f2 | tr -d ' ' || echo "gemini-2.0-flash-exp")
            local ratio=$(grep "^ratio:" "$prompt_file" | cut -d: -f2 | tr -d ' ' || echo "1:1")

            [ -z "$model" ] && model="gemini-2.0-flash-exp"
            [ -z "$ratio" ] && ratio="1:1"

            generate "$prompt" "$model" "$ratio"

            # Markeer als verwerkt
            touch "$processed_file"
            echo ""
        done
        sleep 2
    done
}

# === MAIN ===

case "${1:-}" in
    --watch|-w)
        watch_mode
        ;;
    --help|-h)
        echo "🍌 Nano Banana Pro — One-Click Image Generator"
        echo ""
        echo "Gebruik:"
        echo "  ./nano-banana-generate.sh                        Voert laatste prompt uit uit /prompts"
        echo "  ./nano-banana-generate.sh \"beschrijving\"          Directe prompt"
        echo "  ./nano-banana-generate.sh --watch                Monitor modus (voor Cowork integratie)"
        echo "  ./nano-banana-generate.sh --help                 Dit helpbericht"
        ;;
    "")
        # Zoek laatste prompt bestand
        latest=$(ls -t "$PROMPT_DIR"/*.txt 2>/dev/null | head -1)
        if [ -z "$latest" ]; then
            echo "❌ Geen prompt bestanden gevonden in $PROMPT_DIR"
            echo "   Tip: Gebruik Cowork om een prompt te genereren, of geef een directe beschrijving mee"
            exit 1
        fi
        prompt=$(head -1 "$latest")
        echo -e "${YELLOW}📄 Laatste prompt: $(basename "$latest")${NC}"
        generate "$prompt"
        ;;
    *)
        # Directe prompt als argument
        generate "$1"
        ;;
esac

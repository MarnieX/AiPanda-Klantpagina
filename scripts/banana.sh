#!/bin/bash
# ============================================
# 🍌 banana — De ultieme one-liner
# ============================================
# Optimaliseer + genereer in één commando.
#
# Gebruik:
#   ./banana.sh "een panda in een bamboe bos"
#   ./banana.sh "berglandschap bij zonsopgang" --stijl foto --ratio 16:9
#   ./banana.sh "koffieshop logo" --stijl logo --tekst "Morning Brew"
# ============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$1" ]; then
    echo "🍌 banana — Nano Banana Pro Pipeline"
    echo ""
    echo "Gebruik: ./banana.sh \"beschrijving\" [opties]"
    echo ""
    echo "Opties:"
    echo "  --stijl  cartoon|foto|logo|artistiek  (default: cartoon)"
    echo "  --ratio  1:1|16:9|9:16|4:3|3:4        (default: 1:1)"
    echo "  --tekst  \"Tekst in afbeelding\"         (voor logo's)"
    echo "  --model  gemini model naam              (default: gemini-2.0-flash-exp)"
    echo ""
    echo "Voorbeelden:"
    echo "  ./banana.sh \"een panda die code schrijft\""
    echo "  ./banana.sh \"berglandschap\" --stijl foto --ratio 16:9"
    echo "  ./banana.sh \"tech startup\" --stijl logo --tekst \"NovaTech\""
    exit 0
fi

echo "🍌 === Nano Banana Pro Pipeline ==="
echo ""

# Stap 1: Optimaliseer prompt
echo "📝 Stap 1: Prompt optimaliseren..."
python3 "$SCRIPT_DIR/prompt-optimizer.py" "$@"

echo ""

# Stap 2: Genereer afbeelding
echo "🎨 Stap 2: Afbeelding genereren..."
"$SCRIPT_DIR/nano-banana-generate.sh"

echo ""
echo "🍌 === Pipeline compleet! ==="

#!/bin/bash
# ============================================
# Nano Banana Pro MCP — Lokale Installatie v2
# ============================================
# Voer dit script uit op je eigen machine (niet in Cowork).
# Het configureert de MCP server voor Claude Desktop.
#
# Gebruik:
#   chmod +x setup-nano-banana-mcp.sh
#   ./setup-nano-banana-mcp.sh
# ============================================

set -e

echo "🍌 Nano Banana Pro MCP — Setup v2"
echo "==================================="

# 1. Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js niet gevonden. Installeer via: https://nodejs.org"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# 2. Check npx
if ! command -v npx &> /dev/null; then
    echo "❌ npx niet gevonden. Installeer via: npm install -g npx"
    exit 1
fi
echo "✅ npx beschikbaar"

# 3. Lees API key uit .env
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | grep GEMINI_API_KEY | xargs)
    echo "✅ API key geladen uit .env"
else
    echo "⚠️  Geen .env gevonden in $SCRIPT_DIR"
    read -p "Voer je GEMINI_API_KEY in: " GEMINI_API_KEY
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Geen GEMINI_API_KEY. Maak er een aan op https://aistudio.google.com/apikey"
    exit 1
fi

# 4. Test de API key
echo "🔑 API key testen..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY")

if [ "$RESPONSE" = "200" ]; then
    echo "✅ API key werkt!"
else
    echo "❌ API key geeft HTTP $RESPONSE. Controleer je key."
    exit 1
fi

# 5. Pre-cache het npm package (zonder het te starten)
echo "📦 MCP server package cachen..."
npm cache add @rafarafarafa/nano-banana-pro-mcp 2>/dev/null && echo "✅ Package gecached" || echo "⚠️  Cache overgeslagen (niet erg, npx downloadt automatisch)"

# 6. Schrijf Claude Desktop config automatisch
CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

echo ""
echo "📋 Claude Desktop configureren..."

# Maak directory aan als die niet bestaat
mkdir -p "$CONFIG_DIR"

if [ -f "$CONFIG_FILE" ]; then
    # Config bestaat al — controleer of nano-banana-pro er al in staat
    if grep -q "nano-banana-pro" "$CONFIG_FILE" 2>/dev/null; then
        echo "⚠️  nano-banana-pro staat al in je config."
        echo "   Bestand: $CONFIG_FILE"
        echo "   Controleer of de API key klopt."
    else
        echo "⚠️  Config bestaat al: $CONFIG_FILE"
        echo "   Voeg dit HANDMATIG toe aan het 'mcpServers' blok:"
        echo ""
        echo "    \"nano-banana-pro\": {"
        echo "      \"command\": \"npx\","
        echo "      \"args\": [\"@rafarafarafa/nano-banana-pro-mcp\"],"
        echo "      \"env\": {"
        echo "        \"GEMINI_API_KEY\": \"$GEMINI_API_KEY\""
        echo "      }"
        echo "    }"
    fi
else
    # Nieuw config bestand aanmaken
    cat > "$CONFIG_FILE" << JSONEOF
{
  "mcpServers": {
    "nano-banana-pro": {
      "command": "npx",
      "args": ["@rafarafarafa/nano-banana-pro-mcp"],
      "env": {
        "GEMINI_API_KEY": "$GEMINI_API_KEY"
      }
    }
  }
}
JSONEOF
    echo "✅ Config aangemaakt: $CONFIG_FILE"
fi

echo ""
echo "==================================="
echo "🎉 Setup compleet!"
echo "==================================="
echo ""
echo "Volgende stappen:"
echo "  1. Herstart Claude Desktop (Cmd+Q, dan opnieuw openen)"
echo "  2. Open een chat en typ: 'Genereer een afbeelding van een panda'"
echo "  3. Claude gebruikt nu Nano Banana Pro via de MCP server"
echo ""
echo "💡 De eerste keer dat Claude de server aanroept, downloadt npx"
echo "   het package automatisch. Dit kan ~10 seconden duren."

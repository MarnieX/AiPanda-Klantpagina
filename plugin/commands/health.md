---
description: Controleer of de AI Panda plugin correct geconfigureerd is
allowed-tools: Bash
---

Voer een uitgebreide health check uit voor de AI Panda Klantpagina plugin. Rapporteer de status van alle dependencies en geef concrete oplossingen bij problemen.

```bash
echo "╔══════════════════════════════════════════╗"
echo "║   AI Panda Plugin — Health Check         ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📅 Datum: $(date '+%d %b %Y %H:%M')"
echo "🖥️  Omgeving: $(if [ -d '/sessions' ]; then echo 'Claude Cowork'; else echo 'Lokaal/Desktop'; fi)"
echo "🐍 Python: $(python3 --version 2>&1)"
echo ""

echo "--- API Keys ---"
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✅ GEMINI_API_KEY: aanwezig (${#GEMINI_API_KEY} tekens)"
else
    echo "⚠️  GEMINI_API_KEY: ONTBREEKT"
    echo "   → Oplossing: stel in via Cowork-omgevingsvariabelen of voeg toe aan .env"
fi
echo ""

echo "--- Plugin bestanden ---"
EXCEL=$(find /sessions ~ -maxdepth 10 -name "ai-panda-team.xlsx" 2>/dev/null | head -1)
if [ -n "$EXCEL" ]; then
    echo "✅ Excel (ai-panda-team.xlsx): $EXCEL"
else
    echo "⚠️  Excel (ai-panda-team.xlsx): NIET GEVONDEN"
    echo "   → Oplossing: voer build.sh uit om de plugin opnieuw te bouwen"
fi

SCRIPT=$(find /sessions ~ -maxdepth 10 -name "generate_notion_image.py" 2>/dev/null | head -1)
if [ -n "$SCRIPT" ]; then
    echo "✅ Image script (generate_notion_image.py): $SCRIPT"
else
    echo "⚠️  Image script: niet gevonden (curl-fallback wordt gebruikt)"
fi
echo ""

echo "--- Python dependencies ---"
python3 -c "import openpyxl; print('✅ openpyxl: OK')" 2>/dev/null \
    || echo "⚠️  openpyxl: ontbreekt → pip install openpyxl --break-system-packages"
echo ""

echo "--- Mapstructuur /sessions (voor debug) ---"
if [ -d "/sessions" ]; then
    find /sessions -maxdepth 5 \( -name "*.xlsx" -o -name "*.py" -o -name "*.json" \) 2>/dev/null | head -15
else
    echo "  (geen /sessions directory — lokale omgeving)"
fi
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Health check voltooid                  ║"
echo "╚══════════════════════════════════════════╝"
```

Toon het resultaat overzichtelijk. Geef bij elk probleem een concrete oplossingssugestie.

Controleer ook of de volgende MCP tools beschikbaar zijn en meld de status:
- `notion-create-pages` — voor het aanmaken van Notion-pagina's
- `mcp__claude_ai_Gamma__generate` — voor toekomstvisie-presentaties

Sluit af met een aanbeveling: als alles groen is, kan `/klantpagina` direct worden uitgevoerd. Bij waarschuwingen: geef aan welke stappen worden overgeslagen of terugvallen op een fallback.

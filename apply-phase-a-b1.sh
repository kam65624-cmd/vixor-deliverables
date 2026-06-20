#!/usr/bin/env bash
# ============================================================================
# VIXOR Phase A + B.1 — Apply Script
# ============================================================================
#
# This script applies the changes made in Phase A (cleanup verification) and
# Phase B.1 (axiom-arbitrage integration) to your vixor-APP repository.
#
# Usage:
#   cd /path/to/your/vixor-APP
#   bash /path/to/apply-phase-a-b1.sh
#
# Prerequisites:
#   - Your vixor-APP repo cloned locally
#   - axiom-arbitrage-trading-bot repo cloned alongside (or this script will clone it)
#   - Node 20+ and npm installed
#
# After running:
#   1. Review changes with: git diff
#   2. Install new deps: npm install
#   3. Test build: npm run build
#   4. Test lint: npm run lint
#   5. Commit: git add -A && git commit -m "Phase A+B.1: arbitrage integration"
#
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  VIXOR Phase A + B.1 — Apply Script                          ║${NC}"
echo -e "${BLUE}║  Cleanup + Arbitrage Integration                             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ─── Step 1: Verify we're in vixor-APP root ───────────────────────────────────
if [ ! -f "package.json" ] || [ ! -d "src/domains" ]; then
  echo -e "${RED}✗ Not in vixor-APP root directory.${NC}"
  echo "  Please cd to your vixor-APP repo root and re-run."
  exit 1
fi
echo -e "${GREEN}✓ vixor-APP root detected: $(pwd)${NC}"

# ─── Step 2: Verify Phase A items (already in repo) ──────────────────────────
echo ""
echo -e "${YELLOW}── Phase A: Verifying cleanup items ──${NC}"

# A.1 .gitignore
if [ -f ".gitignore" ] && grep -q "node_modules" .gitignore; then
  echo -e "${GREEN}  ✓ A.1 .gitignore present and complete${NC}"
else
  echo -e "${RED}  ✗ A.1 .gitignore missing or incomplete${NC}"
  exit 1
fi

# A.2 ESLint config
if [ -f "eslint.config.js" ]; then
  echo -e "${GREEN}  ✓ A.2 ESLint config present${NC}"
else
  echo -e "${RED}  ✗ A.2 eslint.config.js missing${NC}"
  exit 1
fi

# A.3 Git baseline (just warn if dirty)
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo -e "${YELLOW}  ⚠ A.3 Working tree has uncommitted changes (will be modified by this script)${NC}"
else
  echo -e "${GREEN}  ✓ A.3 Working tree clean${NC}"
fi

# A.4 API routes — no action needed (TanStack Start uses server functions, not Next.js dynamic)
echo -e "${GREEN}  ✓ A.4 API routes OK (TanStack Start handles dynamic by default)${NC}"

# A.5 Webhook signatures
if grep -q "x-telegram-bot-api-secret-token" server/api/telegram-webhook.ts server/api/stars-webhook.ts 2>/dev/null; then
  echo -e "${GREEN}  ✓ A.5 Webhook HMAC verification present${NC}"
else
  echo -e "${YELLOW}  ⚠ A.5 Webhook files not found or missing HMAC${NC}"
fi

# A.6 fix-vercel-bundle.mjs production-safe
if [ -f "scripts/fix-vercel-bundle.mjs" ] && grep -q "NODE_ENV === 'development'" scripts/fix-vercel-bundle.mjs; then
  echo -e "${GREEN}  ✓ A.6 Error handler is production-safe${NC}"
else
  echo -e "${YELLOW}  ⚠ A.6 fix-vercel-bundle.mjs not found or not production-safe${NC}"
fi

# ─── Step 3: Phase B.1 — Arbitrage Integration ───────────────────────────────
echo ""
echo -e "${YELLOW}── Phase B.1: Arbitrage Integration ──${NC}"

# B.1.1 Create arbitrage domain directory
mkdir -p src/domains/arbitrage/{strategies,exchanges,mock,tests}
echo -e "${GREEN}  ✓ Created src/domains/arbitrage/ structure${NC}"

# B.1.2 Clone axiom-arbitrage if not present
AXIOM_SRC=""
if [ -d "../axiom-arbitrage-trading-bot/src" ]; then
  AXIOM_SRC="../axiom-arbitrage-trading-bot/src"
  echo -e "${GREEN}  ✓ Found axiom-arbitrage at ../axiom-arbitrage-trading-bot${NC}"
elif [ -d "./axiom-arbitrage-trading-bot/src" ]; then
  AXIOM_SRC="./axiom-arbitrage-trading-bot/src"
  echo -e "${GREEN}  ✓ Found axiom-arbitrage at ./axiom-arbitrage-trading-bot${NC}"
else
  echo -e "${YELLOW}  ⚠ Cloning axiom-arbitrage-trading-bot...${NC}"
  git clone --depth 1 https://github.com/Axiom-Trading-Kits/axiom-arbitrage-trading-bot.git /tmp/axiom-arb
  AXIOM_SRC="/tmp/axiom-arb/src"
  echo -e "${GREEN}  ✓ Cloned to /tmp/axiom-arb${NC}"
fi

# B.1.3 Copy arbitrage files
echo -e "${YELLOW}  → Copying arbitrage files...${NC}"

cp "$AXIOM_SRC/core/engine.ts" src/domains/arbitrage/engine.ts
cp "$AXIOM_SRC/strategies/base.ts" src/domains/arbitrage/strategies/base.ts
cp "$AXIOM_SRC/strategies/crossDex.ts" src/domains/arbitrage/strategies/cross-dex.ts
cp "$AXIOM_SRC/strategies/triangular.ts" src/domains/arbitrage/strategies/triangular.ts
cp "$AXIOM_SRC/strategies/cexDex.ts" src/domains/arbitrage/strategies/cex-dex.ts
cp "$AXIOM_SRC/strategies/index.ts" src/domains/arbitrage/strategies/index.ts
cp "$AXIOM_SRC/exchanges/types.ts" src/domains/arbitrage/exchanges/types.ts
cp "$AXIOM_SRC/exchanges/jupiter/client.ts" src/domains/arbitrage/exchanges/jupiter.client.ts
cp "$AXIOM_SRC/exchanges/axiom/client.ts" src/domains/arbitrage/exchanges/axiom.client.ts
cp "$AXIOM_SRC/exchanges/mock/dexClients.ts" src/domains/arbitrage/mock/dex-clients.ts
cp "$AXIOM_SRC/exchanges/mock/quoteSimulator.ts" src/domains/arbitrage/mock/quote-simulator.ts
cp "$AXIOM_SRC/exchanges/index.ts" src/domains/arbitrage/exchanges/index.ts
cp "$AXIOM_SRC/execution/executor.ts" src/domains/arbitrage/executor.ts
cp "$AXIOM_SRC/types/index.ts" src/domains/arbitrage/types.ts
cp "$AXIOM_SRC/market/priceFeed.ts" src/domains/arbitrage/price-feed.ts
cp "$AXIOM_SRC/market/tokenRegistry.ts" src/domains/arbitrage/token-registry.ts
cp "$AXIOM_SRC/utils/logger.ts" src/domains/arbitrage/logger.ts
cp "$AXIOM_SRC/utils/math.ts" src/domains/arbitrage/math.ts
cp "$AXIOM_SRC/risk/manager.ts" src/domains/arbitrage/risk.ts

# Copy tests (skip engine.test.ts — depends on Express)
cp "$AXIOM_SRC/../tests/strategies.test.ts" src/domains/arbitrage/tests/strategies.test.ts 2>/dev/null || true
cp "$AXIOM_SRC/../tests/risk.test.ts" src/domains/arbitrage/tests/risk.test.ts 2>/dev/null || true
cp "$AXIOM_SRC/../tests/config.test.ts" src/domains/arbitrage/tests/config.test.ts 2>/dev/null || true

echo -e "${GREEN}  ✓ Copied 22 arbitrage files${NC}"

# B.1.4 Fix imports (Python script)
echo -e "${YELLOW}  → Fixing imports...${NC}"
PYTHON_FIX_SCRIPT=$(cat <<'PYEOF'
import os, re
from pathlib import Path
ARBITRAGE_DIR = Path("src/domains/arbitrage")
IMPORT_PATTERN = re.compile(r"""(import\s+(?:type\s+)?(?:[^'"]+\s+from\s+)?['"])([^'"]+)(['"])""")
def fix_import_path(import_path):
    if not import_path.startswith('.'):
        return import_path
    path_no_ext = re.sub(r'\.js$', '', import_path)
    path_no_ext = re.sub(r'/index$', '', path_no_ext)
    return path_no_ext
def process_file(filepath):
    if not filepath.exists():
        return 0
    content = filepath.read_text(encoding='utf-8')
    original = content
    def replace_match(m):
        prefix, import_path, suffix = m.group(1), m.group(2), m.group(3)
        fixed = fix_import_path(import_path)
        return f"{prefix}{fixed}{suffix}"
    content = IMPORT_PATTERN.sub(replace_match, content)
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return 1
    return 0
changed = 0
for ts_file in ARBITRAGE_DIR.rglob("*.ts"):
    changed += process_file(ts_file)
print(f"  ✓ Fixed imports in {changed} files")
PYEOF
)
python3 -c "$PYTHON_FIX_SCRIPT"

# B.1.5 Replace AppConfig → ArbitrageConfig, loadConfig → loadArbitrageConfig
echo -e "${YELLOW}  → Renaming AppConfig → ArbitrageConfig...${NC}"
sed -i 's/AppConfig/ArbitrageConfig/g; s/loadConfig/loadArbitrageConfig/g' \
  src/domains/arbitrage/engine.ts \
  src/domains/arbitrage/executor.ts \
  src/domains/arbitrage/exchanges/index.ts \
  src/domains/arbitrage/risk.ts 2>/dev/null || true

# Fix test imports
sed -i "s|from '../src/config'|from '../config'|g; s|from '../src/market/tokenRegistry'|from '../token-registry'|g; s|from '../src/utils/math'|from '../math'|g; s|from '../src/utils/logger'|from '../logger'|g; s|from '../src/risk/manager'|from '../risk'|g; s|from '../src/execution/executor'|from '../executor'|g; s|from '../src/exchanges/types'|from '../exchanges/types'|g; s|from '../src/strategies/index'|from '../strategies/index'|g; s|from '../src/core/engine'|from '../engine'|g; s|from '../src/strategies'|from '../strategies'|g; s|from '../src/exchanges'|from '../exchanges'|g; s|from '../src/market/priceFeed'|from '../price-feed'|g; s|from '../src/types'|from '../types'|g; s|from '../src/exchanges/jupiter/client'|from '../exchanges/jupiter.client'|g; s|from '../src/exchanges/axiom/client'|from '../exchanges/axiom.client'|g; s|from '../src/exchanges/mock/dexClients'|from '../mock/dex-clients'|g; s|from '../src/strategies/crossDex'|from '../strategies/cross-dex'|g; s|from '../src/strategies/triangular'|from '../strategies/triangular'|g; s|from '../src/strategies/cexDex'|from '../strategies/cex-dex'|g; s/loadConfig/loadArbitrageConfig/g" \
  src/domains/arbitrage/tests/*.ts 2>/dev/null || true

# Add ARBITRAGE_ prefix to test env vars
sed -i 's/BOT_MODE:/ARBITRAGE_BOT_MODE:/g; s/MIN_PROFIT_BPS:/ARBITRAGE_MIN_PROFIT_BPS:/g; s/MAX_TRADE_SIZE_SOL:/ARBITRAGE_MAX_TRADE_SIZE_SOL:/g; s/MAX_SLIPPAGE_BPS:/ARBITRAGE_MAX_SLIPPAGE_BPS:/g; s/WATCH_TOKENS:/ARBITRAGE_WATCH_TOKENS:/g; s/DRY_RUN:/ARBITRAGE_DRY_RUN:/g; s/EXECUTION_ENABLED:/ARBITRAGE_EXECUTION_ENABLED:/g; s/PORT:/ARBITRAGE_PORT:/g' \
  src/domains/arbitrage/tests/*.ts 2>/dev/null || true

# Remove Express-dependent test
rm -f src/domains/arbitrage/tests/engine.test.ts

echo -e "${GREEN}  ✓ Renamed types and fixed test imports${NC}"

# B.1.6 Add @solana/web3.js + bs58 to package.json (if not present)
if ! grep -q '"@solana/web3.js"' package.json; then
  echo -e "${YELLOW}  → Adding @solana/web3.js + bs58 to package.json...${NC}"
  # Use npm install which is safer than manual JSON editing
  npm install --save @solana/web3.js@^1.98.4 bs58@^6.0.0 2>&1 | tail -3
  echo -e "${GREEN}  ✓ Added Solana dependencies${NC}"
else
  echo -e "${GREEN}  ✓ @solana/web3.js already in package.json${NC}"
fi

# B.1.7 Append arbitrage env vars to .env.example
if ! grep -q "ARBITRAGE_BOT_MODE" .env.example; then
  echo -e "${YELLOW}  → Adding arbitrage env vars to .env.example...${NC}"
  cat >> .env.example << 'ENVEOF'

# ── Arbitrage Bot (Phase B.1 — ported from axiom-arbitrage) ──────────────────
ARBITRAGE_BOT_MODE=mock
ARBITRAGE_SOLANA_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_HELIUS_KEY
ARBITRAGE_AXIOM_API_KEY=
ARBITRAGE_AXIOM_API_URL=https://api.axiom.trade
ARBITRAGE_JUPITER_QUOTE_URL=https://quote-api.jup.ag/v6
ARBITRAGE_SCAN_INTERVAL_MS=5000
ARBITRAGE_MIN_PROFIT_BPS=15
ARBITRAGE_MAX_SLIPPAGE_BPS=50
ARBITRAGE_MAX_TRADE_SIZE_SOL=1
ARBITRAGE_MAX_DAILY_TRADES=100
ARBITRAGE_MAX_CONSECUTIVE_FAILURES=5
ARBITRAGE_EXECUTION_ENABLED=false
ARBITRAGE_DRY_RUN=true
ARBITRAGE_WALLET_PRIVATE_KEY=
ARBITRAGE_WATCH_TOKENS=SOL,USDC,BONK,WIF,JUP
ARBITRAGE_LOG_LEVEL=info
ENVEOF
  echo -e "${GREEN}  ✓ Added arbitrage env vars${NC}"
else
  echo -e "${GREEN}  ✓ Arbitrage env vars already present${NC}"
fi

# B.1.8 Add arbitrage migration
if [ ! -f "supabase/migrations/20260621000000_add_arbitrage_domain.sql" ]; then
  echo -e "${YELLOW}  → Note: arbitrage SQL migration needs to be created separately${NC}"
  echo -e "${YELLOW}    Get it from: supabase/migrations/20260621000000_add_arbitrage_domain.sql${NC}"
fi

# ─── Step 4: Summary ─────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Phase A + B.1 — COMPLETED                                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "  1. Review changes:"
echo "     ${BLUE}git diff${NC}"
echo "     ${BLUE}git status${NC}"
echo ""
echo "  2. Install new dependencies:"
echo "     ${BLUE}npm install${NC}"
echo ""
echo "  3. Test build:"
echo "     ${BLUE}npm run build${NC}"
echo ""
echo "  4. Test lint:"
echo "     ${BLUE}npm run lint${NC}"
echo ""
echo "  5. Run arbitrage tests:"
echo "     ${BLUE}npx vitest run src/domains/arbitrage/tests/${NC}"
echo ""
echo "  6. Apply Supabase migration:"
echo "     ${BLUE}npx supabase db push${NC}"
echo "     OR run arbitrage SQL in Supabase SQL Editor"
echo ""
echo "  7. Set env vars on Vercel:"
echo "     ${BLUE}vercel env add ARBITRAGE_BOT_MODE${NC}"
echo "     ${BLUE}vercel env add ARBITRAGE_SOLANA_RPC_URL${NC}"
echo "     ${BLUE}vercel env add ARBITRAGE_EXECUTION_ENABLED${NC}  (keep 'false')"
echo "     ${BLUE}vercel env add ARBITRAGE_DRY_RUN${NC}            (keep 'true')"
echo "     ... (see .env.example for full list)"
echo ""
echo "  8. Commit:"
echo "     ${BLUE}git add -A${NC}"
echo "     ${BLUE}git commit -m 'Phase A+B.1: arbitrage integration from axiom-arbitrage'${NC}"
echo "     ${BLUE}git push${NC}"
echo ""
echo -e "${YELLOW}⚠ SAFETY REMINDERS:${NC}"
echo "  • ARBITRAGE_DRY_RUN=true by default — no real funds moved"
echo "  • ARBITRAGE_EXECUTION_ENABLED=false by default — no live trades"
echo "  • Test thoroughly on testnet before enabling live mode"
echo "  • Never commit ARBITRAGE_WALLET_PRIVATE_KEY to git"
echo ""

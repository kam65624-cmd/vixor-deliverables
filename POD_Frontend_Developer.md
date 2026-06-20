# POD — Frontend Developer

> **Role**: Frontend Developer for VIXOR Hybrid Platform
> **Reports to**: Lead Developer
> **Mission**: Build the 3-style Web3 Terminal + Workspace Switcher + all UI components

---

## Responsibilities

### 1. UI Implementation
- Build all pages in `src/routes/_authenticated/`
- Implement 3 design styles (BullX + Axiom + OpenSea)
- Build WorkspaceSwitcher component
- Build all UI components with shadcn/ui + Tailwind 4

### 2. State Management
- Use TanStack Router for routing
- Use TanStack Query for server state
- Use React Context for workspace state
- Use localStorage for preferences

### 3. Performance
- Lazy load all route components
- Code split per workspace
- Optimize images (WebP + lazy)
- Achieve LCP < 2s on all pages

### 4. Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation on all pages
- Screen reader support
- Proper ARIA labels

---

## Phase-by-Phase Tasks

### Phase B.2 — Wallet Hub (Week 3)
- [ ] Install `@solana/wallet-adapter-react` + `wagmi` + `viem`
- [ ] Create `WalletProvider` component (wraps app)
- [ ] Build `WalletConnect` button component
- [ ] Build `WalletModal` (choose wallet)
- [ ] Add wallet state to AppShell context
- [ ] Test: Phantom connect works on Solana
- [ ] Test: MetaMask connect works on EVM
- [ ] Test: session persists across page reloads

### Phase B.3 — Web3 Terminal (Weeks 3-5)

#### B.3.1 — Design System (Week 3)
- [ ] Create `src/experience/styles/bullx.ts` (palette + typography + spacing)
- [ ] Create `src/experience/styles/axiom.ts`
- [ ] Create `src/experience/styles/opensea.ts`
- [ ] Create `src/experience/styles/index.ts` (barrel export)
- [ ] Create shared component primitives (Button, Card, Badge) with 4 variants each
- [ ] Test: each style renders correctly

#### B.3.2 — Workspace Switcher (Week 3)
- [ ] Create `WorkspaceSwitcher` component
- [ ] Add to AppShell header (all pages)
- [ ] Implement slide transition (300ms)
- [ ] Persist state in localStorage
- [ ] Color code: yellow (OS) + cyan (Terminal)
- [ ] Test: switch works, state persists, no layout breaks

#### B.3.3 — Discover Page (Week 4) — Axiom Style
- [ ] Create `src/routes/_authenticated/discover.tsx`
- [ ] Build filters sidebar (6 filters)
- [ ] Build token card grid (responsive)
- [ ] Each card: symbol, price change, volume, liquidity, age, SM%, social score
- [ ] Add VIXOR AI Risk Badge (green/yellow/red)
- [ ] Add NFT Badge (4 states)
- [ ] Real-time updates (30s polling)
- [ ] Test: filters work, cards render, click navigates to token page

#### B.3.4 — Token Page (Week 4) — BullX Style
- [ ] Create `src/routes/_authenticated/token.$symbol.tsx`
- [ ] 3-column layout: Chart (60%) + Order Book/Entry (20%) + Side Panel (20%)
- [ ] Candlestick chart via `lightweight-charts`
- [ ] Order book (5m Vol + Buys/Sells + Net)
- [ ] Order entry (Market/Limit/Adv tabs + Buy/Sell + Amount)
- [ ] Token info (price, 24h, liquidity, supply, ATH)
- [ ] Bottom tabs (Trades/Positions/Orders/Holders)
- [ ] Hotkeys bar + UTC time
- [ ] VIXOR AI overlay (warning banner)
- [ ] NFT Badge + section
- [ ] Test: chart renders, order entry works (dry-run), AI overlay shows

#### B.3.5 — Communities Page (Week 5) — OpenSea Style
- [ ] Create `src/routes/_authenticated/communities.tsx`
- [ ] Collection header (cover + token info + stats)
- [ ] 5 tabs: Overview, Twitter, Telegram, Discord, Reddit
- [ ] Sentiment heatmap (24h, green/red)
- [ ] Top mentions feed
- [ ] Influencer activity
- [ ] Trending tickers
- [ ] Test: all tabs load data, heatmap renders

#### B.3.6 — Wallet Page (Week 5) — OpenSea Style
- [ ] Create `src/routes/_authenticated/wallet.tsx`
- [ ] Wallet header (address + chain + balance + Send/Receive/Swap)
- [ ] Holdings grid (token cards)
- [ ] Activity tab (timeline)
- [ ] Achievements tab (badges)
- [ ] Send/Receive/Swap modals
- [ ] Test: holdings display, modals work, swap executes (dry-run)

#### B.3.7 — Activity Page (Week 5) — OpenSea Style
- [ ] Create `src/routes/_authenticated/activity.tsx`
- [ ] Filter bar (All/Trades/Transfers/Learning/AI Decisions)
- [ ] Activity feed (vertical timeline)
- [ ] VIXOR AI Insights panel
- [ ] Export to CSV
- [ ] Test: feed loads, filters work, AI insights show

### Phase B.4 — Memecoin Discovery UI (Weeks 5-7)
- [ ] Build token card components for Discover page
- [ ] Build VIXOR AI Risk Badge component
- [ ] Build NFT Badge component (4 states)
- [ ] Build NFT section in Token Page
- [ ] Test: all badges render correctly

### Phase C — VIXOR AI UI (Weeks 8-9)
- [ ] Build AI Coach overlay component (Token Page)
- [ ] Build Daily Briefing component (Home page)
- [ ] Build Weekly Report component (Coach page)
- [ ] Build Risk Governor warning component (Order Entry)
- [ ] Build Smart Money alert component (Discover page)
- [ ] Test: all AI overlays show correctly

### Phase C.2 — Knowledge Hub UI (Weeks 10-11)
- [ ] Build Learning Hub pages (3 paths + 37 lessons)
- [ ] Build Calendar Hub page
- [ ] Build News Hub page
- [ ] Build Decisions Hub page
- [ ] Test: all pages functional

### Phase D — Polish (Weeks 12-14)
- [ ] Performance optimization (code splitting, lazy loading)
- [ ] Mobile responsive (all pages)
- [ ] PWA update (service worker)
- [ ] Lighthouse score > 90

---

## KPIs

| Metric | Target |
|--------|--------|
| LCP (Largest Contentful Paint) | < 2s |
| FID (First Input Delay) | < 100ms |
| CLS (Cumulative Layout Shift) | < 0.1 |
| Lighthouse score | > 90 |
| Console errors | 0 |
| Bundle size (initial, gzipped) | < 500KB |

---

## Quality Gates

1. Component renders without console errors
2. Responsive on mobile (375px) + tablet (768px) + desktop (1440px)
3. Dark mode works (default)
4. Keyboard navigation works
5. Loading states show
6. Error states show
7. All tests pass (Vitest + Playwright)

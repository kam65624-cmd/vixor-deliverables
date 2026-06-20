# POD — AI/ML Engineer

> **Role**: AI/ML Engineer for VIXOR Hybrid Platform
> **Reports to**: Lead Developer
> **Mission**: Build the 4 VIXOR AI agents, LLM prompts, and personalization engine

---

## Responsibilities

### 1. AI Agent Development
- Build 4 VIXOR AI agents (Coach + Analyst + Governor + Hunter)
- Design LLM prompts for each agent
- Implement agent orchestration
- Tune prompts based on user feedback

### 2. Personalization Engine
- Extend `user_memories` schema
- Build Behavioral Profile builder
- Implement adaptive UI logic
- Implement personalized alerts

### 3. LLM Management
- Maintain LLMRouter (4 providers: ZAI + OpenAI + Anthropic + Groq)
- Implement fallback chains
- Monitor LLM costs + latency
- Optimize token usage

### 4. AI Quality
- Measure agent accuracy
- Implement feedback loops
- A/B test prompts
- Track user satisfaction

---

## Phase-by-Phase Tasks

### Phase C.1 — VIXOR AI 4 Agents (Weeks 8-9)

#### C.1.1 — Real-time Coach (Week 8)
- [ ] Design Coach prompt (system + user context)
- [ ] Build `src/domains/copilot/server/coach.agent.ts`
- [ ] Implement real-time overlay trigger (on trade preview)
- [ ] Integrate with `user_memories` (last 30 days)
- [ ] Implement latency target (< 2s)
- [ ] Build UI overlay component (with Frontend dev)
- [ ] Test: Coach comments on 80%+ of trades
- [ ] KPI: latency < 2s, 60%+ users read overlay

#### C.1.2 — Behavioral Analyst (Week 8)
- [ ] Design Analyst prompt (weekly pattern analysis)
- [ ] Build `src/domains/copilot/server/analyst.agent.ts`
- [ ] Implement cron job (Sunday 08:00 UTC)
- [ ] Analyze 7-30 days of `user_memories`
- [ ] Use Anthropic Claude (advanced reasoning)
- [ ] Generate 4-section report (stats + patterns + recommendations + learning)
- [ ] Store report in `vixor_decisions` table
- [ ] Send via NotificationRouter (telegram + email + in-app)
- [ ] Test: report generates correctly, delivers on time
- [ ] KPI: 100% delivery to active users, 50%+ read rate

#### C.1.3 — Risk Governor (Week 9)
- [ ] Design Governor prompt (risk assessment)
- [ ] Build `src/domains/copilot/server/governor.agent.ts`
- [ ] Build user Risk Profile schema:
  ```
  { style, tolerance, weakness, strength, preferred_chains, preferred_tokens, active_hours, avg_session }
  ```
- [ ] Implement profile builder (weekly update from `user_memories`)
- [ ] Implement block/warn/allow logic in Order Entry
- [ ] Implement personalized alerts (not generic)
- [ ] Test: Governor blocks risky trades, warns medium-risk
- [ ] KPI: 30%+ acceptance rate for suggestions

#### C.1.4 — Smart Money Hunter (Week 9)
- [ ] Design Hunter prompt (opportunity scoring)
- [ ] Build `src/domains/copilot/server/hunter.agent.ts`
- [ ] Implement hourly scan (Helius RPC + Birdeye)
- [ ] Track top 100 smart money wallets
- [ ] Detect collective buying patterns
- [ ] Score opportunities (0-100)
- [ ] Send alerts via NotificationRouter
- [ ] Add markers on Token Page chart
- [ ] Test: alerts trigger on smart money inflows
- [ ] KPI: 55%+ win rate on alerts

#### C.1.5 — Feedback Loop (Week 9)
- [ ] Build `acceptDecision` server function
- [ ] Build `rejectDecision` server function
- [ ] Store feedback in `vixor_decisions` table
- [ ] Update agent prompts based on feedback
- [ ] Track accuracy metrics per agent
- [ ] Test: feedback recorded, agents improve

### Phase C.2 — Knowledge Hub AI (Weeks 10-11)
- [ ] Implement LLM news classification (macro/crypto/token-specific)
- [ ] Implement sentiment scoring (positive/negative/neutral)
- [ ] Implement importance scoring (1-5)
- [ ] Implement personal impact analysis (how news affects user's portfolio)
- [ ] Implement Calendar AI alerts (24h before events)
- [ ] Implement Learning path recommendations (based on user weaknesses)
- [ ] Test: classification accurate, alerts trigger

### Phase D — AI Polish (Weeks 12-14)
- [ ] A/B test prompts (compare accuracy)
- [ ] Optimize token usage (reduce costs)
- [ ] Implement streaming for Coach (real-time typing)
- [ ] Add AI accuracy dashboard
- [ ] Monitor LLM costs per user
- [ ] Test: streaming works, costs within budget

---

## KPIs

| Metric | Target |
|--------|--------|
| Coach engagement (overlay views) | 60%+ of trades |
| Coach latency | < 2s |
| Analyst report delivery | 100% of active users (weekly) |
| Analyst report read rate | 50%+ |
| Governor suggestion acceptance | 30%+ |
| Hunter alert win rate | 55%+ |
| Hunter alerts per day | 5+ |
| LLM cost per user/month | < $5 |
| AI accuracy (overall) | > 75% |

---

## Prompt Design Standards

### 1. System Prompt Structure
```
You are [AGENT_NAME], a [ROLE_DESCRIPTION] for VIXOR trading platform.

Your mission: [MISSION]

User context:
- Trading style: {style}
- Risk tolerance: {tolerance}
- Known weaknesses: {weaknesses}
- Known strengths: {strengths}

Recent behavior (last 30 days):
{user_memories_summary}

Rules:
1. [RULE_1]
2. [RULE_2]
...

Output format: [JSON_SCHEMA_OR_TEXT_FORMAT]
```

### 2. Prompt Versioning
- Version all prompts (e.g., `coach-v1.0`, `coach-v1.1`)
- Store version in `vixor_decisions` table
- A/B test new versions before full rollout
- Rollback if accuracy drops

### 3. Token Optimization
- Use `max_tokens` parameter wisely
- Compress user_memories (summary, not raw)
- Use system prompts efficiently (cache when possible)
- Choose model based on task complexity (ZAI for simple, Claude for complex)

---

## Quality Gates

1. All prompts versioned + documented
2. All agents have unit tests (mock LLM)
3. All agents have integration tests (real LLM, dry-run)
4. Feedback loop implemented
5. Accuracy metrics tracked
6. LLM costs monitored
7. No PII in prompts sent to external LLMs

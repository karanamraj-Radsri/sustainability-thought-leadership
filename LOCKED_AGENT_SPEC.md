# 🔒 LOCKED AGENT SPECIFICATION

**Last Updated:** 2026-02-23 21:30:48
**Status:** FINAL - NO CHANGES WITHOUT APPROVAL
**Author:** karanamraj-Radsri & Copilot

---

## AGENT 1: trend_detector.py

### Purpose
Fetch real-world articles from NewsAPI and identify emerging trends with GPT analysis.

### Input
- **API Keys (from .env):**
  - OPENAI_API_KEY (for GPT-4o-mini)
  - NEWSAPI_KEY (for article fetching)
  - GITHUB_TOKEN (for future integration)

- **Fixed Topics (LOCKED - DO NOT CHANGE):**
  1. Circular Economy
  2. Carbon Management
  3. CSRD/CSDDD Compliance
  4. Sustainable Materials

### Processing

**Step 1: Article Fetching**
- Search NewsAPI for EACH topic
- Fetch: **10 articles per topic**
- **Total: 40 articles** (10 × 4 topics)
- **Timeframe: Last 7 days (WEEKLY)**

**Step 2: Per-Article Analysis**
For EACH of 40 articles, extract:
- Title
- URL
- Source (from NewsAPI)
- Published Date

**Step 3: GPT Analysis**
Use GPT-4o-mini to:
- Identify: What TREND does this article represent?
- Summarize: 5 key bullet point takeaways
- Assess: Relevance to Sreepad's expertise (polymers/materials/compliance)

### Output Files

**File 1: Markdown (Human-Readable)**
```
research/# Trending Topics - Week X (Date Range) - RAW_DATA.md
```

**File 2: JSON (Machine-Readable for Agent 2)**
```
research/week-X-trends-raw.json
```

**JSON Schema:**
```json
{
  "week": INTEGER,
  "date_range": "STRING (Feb 23-28, 2026)",
  "scan_date": "DATETIME",
  "timeframe_days": 7,
  "articles_total": 40,
  "articles_per_topic": 10,
  "topics": ["Circular Economy", "Carbon Management", "CSRD/CSDDD Compliance", "Sustainable Materials"],
  "articles": [
    {
      "article_id": INTEGER,
      "topic": "STRING",
      "title": "STRING",
      "url": "STRING (valid URL)",
      "source": "STRING",
      "published_date": "DATE",
      "gpt_identified_trend": "STRING",
      "key_takeaways": ["STRING", "STRING", "STRING", "STRING", "STRING"],
      "relevance_to_sreepad": "HIGH|MEDIUM|LOW",
      "relevance_explanation": "STRING"
    }
  ]
}
```

### Execution
```bash
python scripts/trend_detector.py
```

**Outputs:**
- ✅ `research/# Trending Topics - Week X - RAW_DATA.md`
- ✅ `research/week-X-trends-raw.json`
- ✅ Console progress output
- ❌ NO GitHub Issue (Agent 2 creates it)

### Locked Parameters
| Parameter | Value | Locked |
|-----------|-------|--------|
| Articles per topic | 10 | 🔒 |
| Total articles | 40 | 🔒 |
| Topics | 4 (Circular Economy, Carbon Management, CSRD/CSDDD, Sustainable Materials) | 🔒 |
| Timeframe | 7 days (weekly) | 🔒 |
| GPT Model | gpt-4o-mini | 🔒 |
| Key Takeaways | 5 bullet points | 🔒 |
| Output Formats | Markdown + JSON | 🔒 |

---

## AGENT 2: trend_curator.py

### Purpose
Analyze, score, rank, and curate trends from Agent 1's raw data. Show all trends for human verification.

### Input
- **Files from Agent 1:**
  - `research/# Trending Topics - Week X - RAW_DATA.md`
  - `research/week-X-trends-raw.json`

- **API Keys (from .env):**
  - OPENAI_API_KEY (for scoring)
  - GITHUB_TOKEN (for GitHub Issue creation)

### Processing

**Step 1: Parse Agent 1 Output**
- Load JSON file
- Extract all 40 articles + identified trends

**Step 2: Manual Deduplication Verification**
- Display ALL 40 identified trends in raw list
- **NO auto-deduplication**
- Purpose: Human verification of trend quality
- You review and identify duplicates manually

**Step 3: Score Each Unique Trend**
Use GPT-4o-mini to assign scores (0-100) for:

- **Relevance (40% weight):** How relevant to Sreepad's expertise?
  - Polymers/materials science
  - Regulatory compliance (CSRD, CSDDD, EUDR)
  - Circular economy & sustainability

- **Timeliness (30% weight):** How urgent/recent is this trend?
  - Is it happening NOW (2026)?
  - Will it impact business soon?

- **Novelty (20% weight):** How new/emerging is it?
  - Is it established knowledge or breakthrough?

- **Actionability (10% weight):** Can Sreepad advise on it?
  - Can he provide thought leadership?
  - Is it actionable for executives?

**Scoring Formula:**
```
Final Score = (Relevance × 0.4) + (Timeliness × 0.3) + (Novelty × 0.2) + (Actionability × 0.1)
```

**Step 4: Rank & Select Top 3**
- Sort all trends by Final Score (highest first)
- **Select Top 3 highest-scoring trends**
- Keep all others for reference

**Step 5: Create GitHub Issue**
- Auto-create GitHub Issue with final markdown
- Title: "Week X Trending Topics - Review & Approve"
- Body: Complete markdown (Top 3 + all others)
- Labels: `trend-review`
- Assignee: karanamraj-Radsri

### Output Files

**File 1: Final Markdown (For LinkedIn Content)**
```
research/# Trending Topics - Week X (Feb 23-28, 2026).md
```

**Markdown Structure:**
```markdown
# Trending Topics - Week X (Feb 23-28, 2026)

## 📊 Curation Metadata
- Curation Date: [DATETIME]
- Articles Analyzed: 40
- Unique Trends Identified: [X]
- Scoring Criteria: Relevance (40%), Timeliness (30%), Novelty (20%), Actionability (10%)
- Status: ✅ Ranked & Ready for Review

---

## 🥇 TOP 3 SELECTED TRENDS (RANKED)

### TREND #1: [Trend Name]
**Final Score: XX.X/100** ✨ SELECTED

**Scoring Breakdown:**
- Relevance (40%): XX/100 = XX.X points
- Timeliness (30%): XX/100 = XX.X points
- Novelty (20%): XX/100 = XX.X points
- Actionability (10%): XX/100 = XX.X points
- **Total: XX.X/100**

**Why #1:** [GPT explanation]

**Description:** [2-3 sentences]

**Supporting Articles:**
- [Article 1 Title](URL)
- [Article 2 Title](URL)
- [Article 3 Title](URL)

**Recommendation:** [Brief guidance]

---

### TREND #2: [Trend Name]
**Final Score: XX.X/100** ✨ SELECTED
[Same structure]

---

### TREND #3: [Trend Name]
**Final Score: XX.X/100** ✨ SELECTED
[Same structure]

---

## 📋 ALL OTHER TRENDS CAPTURED (For Your Review)

**Note:** These did not rank in top 3. Review to verify trend detection quality.

### Trend #4: [Name]
- Final Score: XX.X/100
- Supporting Articles: [List]
- Summary: [1 sentence]

### Trend #5: [Name]
...

(All remaining trends listed)

---

## ✅ Review Checklist
- [ ] Do Top 3 align with your expertise?
- [ ] Are scores fair?
- [ ] Any trends to swap?
- [ ] Ready for content_generator.py?

_Generated by trend_curator.py_
```

### Execution
```bash
python scripts/trend_curator.py
```

**Outputs:**
- ✅ `research/# Trending Topics - Week X (Feb 23-28, 2026).md`
- ✅ GitHub Issue created (assigned to you)
- ✅ Console progress output

### Locked Parameters
| Parameter | Value | Locked |
|-----------|-------|--------|
| Scoring Criteria | Relevance (40%), Timeliness (30%), Novelty (20%), Actionability (10%) | 🔒 |
| Top trends to select | 3 | 🔒 |
| Auto-deduplication | NO (manual verification) | 🔒 |
| GPT Model | gpt-4o-mini | 🔒 |
| GitHub Issue creation | YES | 🔒 |
| GitHub Issue label | trend-review | 🔒 |
| Timeframe | 7 days (weekly) | 🔒 |

---

## DATA FLOW

```
NewsAPI (40 articles, 7-day window)
        ↓
┌─────────────────────────────────────┐
│   AGENT 1: trend_detector.py        │
│ • Fetch 10 articles per topic       │
│ • GPT: Identify trend per article   │
│ • GPT: 5-bullet summary             │
│ • Assess relevance to Sreepad       │
└─────────────────────────────────────┘
        ↓
   RAW_DATA.md + week-X-trends-raw.json
        ↓
┌─────────────────────────────────────┐
│   AGENT 2: trend_curator.py         │
│ • Parse JSON from Agent 1           │
│ • Show all 40 trends (manual review)│
│ • GPT: Score each trend (4 criteria)│
│ • Rank by Final Score               │
│ • Select Top 3                      │
│ • Create GitHub Issue               │
└─────────────────────────────────────┘
        ↓
   Final Ranked Markdown + GitHub Issue
        ↓
   YOU: Review & Approve in GitHub
        ↓
   Agent 3: content_generator.py (uses Top 3)
```

---

## EXECUTION SCHEDULE (Weekly Cycle)

**Monday-Thursday:**
```bash
python scripts/trend_detector.py
```
Output: RAW_DATA files ready

**Friday Morning:**
```bash
python scripts/trend_curator.py
```
Output: GitHub Issue with ranked Top 3

**Friday (Your Review):**
- Open GitHub Issue
- Review Top 3 + all others
- Comment: "✅ APPROVED"

**Friday Afternoon:**
```bash
python scripts/content_generator.py
```
Output: Draft LinkedIn content

---

## CRITICAL NOTES

🔒 **These parameters are LOCKED. Do not change without explicit approval:**
- Timeframe: 7 days (WEEKLY) - NOT 30 days
- Articles: 40 total (10 per topic)
- Topics: 4 (fixed, locked)
- Top trends: 3 (for content_generator.py)
- Scoring: Relevance 40%, Timeliness 30%, Novelty 20%, Actionability 10%
- Manual verification: ALL 40 trends shown for human review

---

**Document Status: LOCKED - Reference in all future work
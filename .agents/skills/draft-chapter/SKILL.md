---
name: draft-chapter
description: Plans and drafts a 3,000-word chapter scene-by-scene using an unfolding-mystery chain, fact sheet, concept ledger, and 4–6 plate visual plan.
---

# Skill: Draft Chapter

When invoked with a chapter ID (e.g., `/draft-chapter ch01`):

1. **Context Load:** Read `syllabus/style-anchor.md`, `ledger/concepts.json`, the chapter target in `syllabus/master-outline.md`, `.agents/rules/lexicon-style.md`, `.agents/rules/diagram-standards.md`, and `research/<chapter_id>-fact-sheet.md`.
2. **Scene, Mystery Chain & Visual Plan (Stop for Approval):** Propose a 4-section chapter blueprint (~750 words per section, ~3,000 words total):
   - Explicitly list **prior concepts** reused from `ledger/concepts.json` and the **newly earned bolded concepts** that the chapter's causal chain requires.
   - **Unfolding-Mystery Chain Map (Mandatory):** For every section and every major sub-beat, map out:
     `Mystery / Problem Opened → Exact Beat That Solves It → Next Mystery / Tension Handed Off`
     Verify before drafting that **zero** raised difficulties are skipped, deferred silently, or hand-waved away.
   - *Section 1:* A concrete physical problem in time and place (an artifact, a river flood, a quarry) that unfolds into a clear prize and a sharp coordination/engineering mystery handing off to Section 2.
   - *Section 2:* Directly solves Section 1's closing mystery via an economic or social mechanism, then exposes the next scaling bottleneck (memory, trust, scarcity).
   - *Section 3:* Solves the scaling/material/enforcement mystery through engineering, trade, or statecraft—showing who paid the cost.
   - *Section 4:* Uncovers the hidden trade-off or structural limit (e.g., soil salt, debt, bottlenecks), ties the chapter's specific tools and trade-offs together without inflating them into a universal framework, and plants the opening mystery of the next chapter.
   - **Visual Plate Plan (4–6 focused graphics, ~1 every 500–650 words):** Specify each plate's filename (`diagrams/<chapter_id>-<slug>.svg`), type (Regional Map, Engineering/Tool Cutaway, Artifact Field Plate, System Loop, Data Chart), exact prose insertion point (section + paragraph), and grounded facts it will visualize.
   **STOP and wait for user approval on the plan before drafting prose.**
3. **Sequential Section Drafting:** Draft one section at a time into `manuscript/<chapter_id>-<slug>.md`, strictly matching the cadence, physical specificity, unfolding-mystery logic, and lexical level of `syllabus/style-anchor.md` and `.agents/rules/lexicon-style.md`.
   - Never pull unverified numbers, dates, or hypothetical counts into prose—every quantitative claim must trace to `research/<chapter_id>-fact-sheet.md`.
   - Keep chronological eras clearly distinguished when a chapter spans multiple centuries.
   - Reserve bold formatting strictly for the chapter's newly earned systemic concepts.
   - Maintain **Scope Humility**: present the chapter's mechanisms as concrete local examples rather than a grand universal formula or checklist for all civilizations.
   - After drafting all 4 sections, run a quick Python rhythm & banned-word check to confirm ~3,000 words and 14–18 words/sentence average before proceeding to `/illustrate-chapter <chapter_id>` and `/audit-chapter <chapter_id>`.

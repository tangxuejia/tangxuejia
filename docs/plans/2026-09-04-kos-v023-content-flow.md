# KOS V0.23 Single-Source Content and Case Flow Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the KOS V0.23 case experience use the current catalog/Supabase case data as one source of truth, present a stable age-appropriate flow, and close every solved case with correct feedback, sensory practice, and reporting.

**Architecture:** Keep the existing single-file app and current catalog/cloud APIs, but replace late DOM wrappers with one canonical `openCase`, one sensory renderer, and one submit path. Derive story, evidence, workbench instructions, and transfer practice from the selected case plus selected variant; use cloud validation when available and local validation only when a compatible local answer exists, with explicit degraded status.

**Tech Stack:** Static HTML, inline CSS, browser JavaScript, localStorage, Supabase REST/RPC, PowerShell, Node.js syntax checks, Playwright/browser smoke checks where available.

---

### Task 1: Establish a reproducible baseline

**Files:**
- Read: `kos-v023/index.html`
- Create: `docs/plans/2026-09-04-kos-v023-content-flow.md`

**Steps:**

1. Record the latest `master` commit and existing wrapper/symbol locations.
2. Run JavaScript syntax validation against the inline script.
3. Inspect catalog loading, variant selection, answer readers, and cloud validator paths before editing.

### Task 2: Consolidate the case content source and render order

**Files:**
- Modify: `kos-v023/index.html`

**Steps:**

1. Remove the old-story priority from `caseStoryHTML`, `lowGradeStoryHTML`, and `midGradeStoryHTML`; use the selected catalog case and selected variant for title, NPC, background, prompt, evidence, and result.
2. Replace the layered `openCase` overrides with one canonical render path in this order: story/person → question → variant evidence → sensory action → workbench/answer submission → feedback/standard answer/explanation → case-specific family practice.
3. Keep Reality Portal out of the pre-answer path and expose it only after completion where the existing app supports it.
4. Preserve long-case and cloud APIs while avoiding duplicate DOM insertion and timer-based mounting.

### Task 3: Make age bands and workbench semantics accurate

**Files:**
- Modify: `kos-v023/index.html`

**Steps:**

1. Make grades 1–2 show one short, speakable step at a time with icon evidence cards and only key-word pinyin.
2. Make grades 3–4 retain only key evidence and explain the selected variant; keep grades 5–6 on the complete story/mechanism/open task; keep the parent view professional.
3. Generate workbench instructions from the interaction/mechanic semantics for `single`, `multi`, `number`, `plan`, and `time`; for plan tasks split hard-constraint filtering, final choice, and reason into separate steps.

### Task 4: Tie sensory practice and reporting to each case

**Files:**
- Modify: `kos-v023/index.html`

**Steps:**

1. Derive the sensory mission from the current case evidence, interaction, mechanic, or reasoning action instead of a fixed five-case bucket.
2. Record `done`, `difficult`, and `skipped` per case; ensure difficult/skipped never changes correctness or rewards.
3. Surface per-case sensory outcomes in the parent report in addition to aggregate counts.

### Task 5: Harden submit feedback and degraded validation

**Files:**
- Modify: `kos-v023/index.html`

**Steps:**

1. Preserve one submit handler with busy protection and clear incomplete-answer validation.
2. On success, show the standard answer, explanation/reason, and the case-specific family sensory practice before archive completion.
3. Distinguish server validation, compatible local fallback, and unavailable validation; never auto-pass an open question with no local standard answer.
4. Keep server/RLS/auth errors visible as degraded or failed states rather than silently treating them as correct.

### Task 6: Verify and deliver

**Files:**
- Verify: `kos-v023/index.html`

**Steps:**

1. Run syntax checks after each implementation batch and a final check.
2. Exercise cases `001`, `006`, `011`, `016`, `021`, `026`, `030` and all five interaction types through the browser or a deterministic DOM harness.
3. Smoke-test grades 1–2, 3–4, and 5–6, including no blank screen, duplicate controls, dead buttons, or repeated click submission.
4. Inspect the public Pages URL after pushing and record any checks that require a real authenticated account.
5. Commit the focused change and push `master`.

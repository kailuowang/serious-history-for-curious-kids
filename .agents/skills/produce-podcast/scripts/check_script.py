#!/usr/bin/env python3
"""Telemetry & style linter for podcast scripts (podcasts/chXX-script.md).

Usage:
    python3 .agents/skills/produce-podcast/scripts/check_script.py ch01
    python3 .agents/skills/produce-podcast/scripts/check_script.py podcasts/ch01-script.md
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

BANNED_CORNY_PHRASES = [
    r"\bmind blown\b",
    r"\bpop quiz\b",
    r"\bcan you imagine\b",
    r"\bbuckle up\b",
    r"\blet'?s dive in\b",
    r"\bthat'?s wild\b",
    r"\bwait[—\-, ]+what\b",
    r"\bhaha\b",
    r"\blove that\b",
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\bcrucially\b",
    r"\ba testament to\b",
    r"\btapestry\b",
    r"\bdelve\b",
    r"\bmonumental feat\b",
    r"\bbustling\b",
]

UNANCHORED_ERA_LABELS = [
    r"\bUr III\b",
    r"\bOld Babylonian\b",
    r"\bUruk III\b",
    r"\bLate Uruk\b",
    r"\bEarly Dynastic\b",
    r"\bMiddle Kingdom\b",
    r"\bOld Kingdom\b",
    r"\bLate Antiquity\b",
]

VALID_VOCAL_TAGS = {
    "soft laugh",
    "sighs",
    "short pause",
    "warmly",
    "thoughtfully",
    "gently",
    "cheerfully",
}

TURN_RE = re.compile(r"^\*\*(Amy|Sam):\*\*\s*(.+)$")
ACT_RE = re.compile(r"^##\s+(.+)$")
TAG_RE = re.compile(r"\[([^\]]+)\]")


def strip_tags(text: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub("", text)).strip()


def resolve_script_path(arg: str) -> tuple[Path, str | None]:
    p = Path(arg)
    if p.exists():
        m = re.search(r"(ch\d+)", p.name)
        return p, (m.group(1) if m else None)
    candidate = REPO_ROOT / "podcasts" / f"{arg}-script.md"
    if candidate.exists():
        return candidate, arg
    raise FileNotFoundError(f"Could not find script at '{arg}' or '{candidate}'")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_script.py <chXX | path/to/chXX-script.md>")
        return 2

    script_path, chapter_id = resolve_script_path(sys.argv[1])
    lines = script_path.read_text(encoding="utf-8").splitlines()

    acts: list[dict] = []
    current_act: dict | None = None
    turns: list[dict] = []
    unknown_tags: list[tuple[int, str]] = []
    exclamations: list[tuple[int, str]] = []
    banned_hits: list[tuple[int, str, str]] = []
    era_hits: list[tuple[int, str, str]] = []

    for lineno, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        act_m = ACT_RE.match(line)
        if act_m:
            current_act = {"title": act_m.group(1).strip(), "turns": [], "words": 0}
            acts.append(current_act)
            continue

        turn_m = TURN_RE.match(line)
        if turn_m:
            speaker, body = turn_m.group(1), turn_m.group(2).strip()
            for tag in TAG_RE.findall(body):
                if tag.lower() not in VALID_VOCAL_TAGS:
                    unknown_tags.append((lineno, tag))
            spoken = strip_tags(body)
            words = len(spoken.split())
            turn = {
                "line": lineno,
                "speaker": speaker,
                "words": words,
                "text": spoken,
                "tags": TAG_RE.findall(body),
            }
            turns.append(turn)
            if current_act is not None:
                current_act["turns"].append(turn)
                current_act["words"] += words

            if "!" in spoken:
                exclamations.append((lineno, spoken[:100]))
            for pat in BANNED_CORNY_PHRASES:
                if re.search(pat, spoken, re.IGNORECASE):
                    banned_hits.append((lineno, pat, spoken[:100]))
            for pat in UNANCHORED_ERA_LABELS:
                if re.search(pat, spoken):
                    era_hits.append((lineno, pat, spoken[:100]))

    if not turns:
        print(f"ERROR: No '**Amy:**' or '**Sam:**' turns found in {script_path}")
        return 1

    total_words = sum(t["words"] for t in turns)
    amy_words = sum(t["words"] for t in turns if t["speaker"] == "Amy")
    sam_words = sum(t["words"] for t in turns if t["speaker"] == "Sam")
    est_minutes = total_words / 150.0
    turn_lengths = [t["words"] for t in turns]
    avg_turn = statistics.mean(turn_lengths)
    stdev_turn = statistics.stdev(turn_lengths) if len(turn_lengths) > 1 else 0.0
    total_tags = sum(len(t["tags"]) for t in turns)
    amy_pct = (amy_words / total_words) * 100
    sam_pct = (sam_words / total_words) * 100

    try:
        display_path = str(script_path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        display_path = str(script_path)
    print(f"=== Podcast Script Telemetry: {display_path} ===")
    print(f"Acts:            {len(acts)}")
    print(f"Total turns:     {len(turns)}")
    print(f"Total words:     {total_words} (target: 1,800–2,250)")
    print(f"Est. runtime:    {est_minutes:.1f} min @ 150 wpm (target: 12.0–15.0 min)")
    print(f"Speaker share:   Amy {amy_pct:.1f}% ({amy_words}w) | Sam {sam_pct:.1f}% ({sam_words}w)")
    print(f"Turn length:     avg {avg_turn:.1f} words, stdev {stdev_turn:.1f} (min {min(turn_lengths)}, max {max(turn_lengths)})")
    print(f"Vocal tags:      {total_tags} ({total_tags / max(len(turns), 1):.2f}/turn; target ~0.10–0.18)")

    print("\n--- Per-Act Breakdown (target 250–500 words/act for clean Gemini TTS chunks) ---")
    warnings = 0
    for idx, act in enumerate(acts):
        flag = ""
        if act["words"] > 560:
            flag = "  [WARN: long act — consider splitting for steady TTS room tone]"
            warnings += 1
        print(f"  Act {idx}: {act['title']} — {act['words']}w ({len(act['turns'])} turns){flag}")

    # Concept coverage check
    concepts_path = REPO_ROOT / "ledger" / "concepts.json"
    missing_concepts: list[str] = []
    if chapter_id and concepts_path.exists():
        ledger = json.loads(concepts_path.read_text(encoding="utf-8"))
        full_text = " ".join(t["text"] for t in turns).lower()
        ch_concepts = [
            c["term"]
            for c in ledger.get("introduced_concepts", [])
            if c.get("chapter") == chapter_id
        ]
        for term in ch_concepts:
            if not re.search(rf"\b{re.escape(term.lower())}(?:s|es)?\b", full_text):
                missing_concepts.append(term)
        print(f"\n--- Chapter Concepts ({chapter_id}) ---")
        print(f"  Required: {', '.join(ch_concepts) or '(none listed)'}")
        if missing_concepts:
            print(f"  MISSING:  {', '.join(missing_concepts)}")
            warnings += len(missing_concepts)
        else:
            print("  Status:   All concepts present.")

    # Rule checks
    print("\n--- Style & Audio Checks ---")
    if not (1650 <= total_words <= 2450):
        print(f"  [WARN] Total words ({total_words}) outside comfortable 1,800–2,250 window.")
        warnings += 1
    if sam_pct < 18.0 or sam_pct > 45.0:
        print(f"  [WARN] Speaker balance outside Historian/Inquirer target (Sam {sam_pct:.1f}%). Target Amy 60%–80% / Sam 20%–40%.")
        warnings += 1
    if stdev_turn < 6.0:
        print(f"  [WARN] Turn lengths look uniform (stdev {stdev_turn:.1f}); vary short pushbacks and fuller explanations.")
        warnings += 1
    if exclamations:
        print(f"  [WARN] Found {len(exclamations)} exclamation mark(s):")
        for ln, snippet in exclamations[:8]:
            print(f"         L{ln}: {snippet}")
        warnings += len(exclamations)
    if banned_hits:
        print(f"  [WARN] Banned corny/LLM phrases ({len(banned_hits)}):")
        for ln, pat, snippet in banned_hits[:10]:
            print(f"         L{ln} ({pat}): {snippet}")
        warnings += len(banned_hits)
    if era_hits:
        print(f"  [WARN] Unanchored era shorthand ({len(era_hits)}):")
        for ln, pat, snippet in era_hits[:10]:
            print(f"         L{ln} ({pat}): {snippet}")
        warnings += len(era_hits)
    if unknown_tags:
        print(f"  [WARN] Undocumented vocal tags ({len(unknown_tags)}):")
        for ln, tag in unknown_tags:
            print(f"         L{ln}: [{tag}]")
        warnings += len(unknown_tags)

    if warnings == 0:
        print("  PASS — Zero warnings.")
        return 0
    print(f"\nFinished with {warnings} warning(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

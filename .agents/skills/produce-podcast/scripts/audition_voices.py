#!/usr/bin/env python3
"""Render Amy & Sam voice-pair auditions (+ optional Lyria theme music candidates)
and build an offline interactive HTML player at podcasts/auditions/audition-player.html.

Usage:
    python3 .agents/skills/produce-podcast/scripts/audition_voices.py
    python3 .agents/skills/produce-podcast/scripts/audition_voices.py --model gemini-3.8-flash-tts
    python3 .agents/skills/produce-podcast/scripts/audition_voices.py --voices-only
    python3 .agents/skills/produce-podcast/scripts/audition_voices.py --dry-run
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _tts_core import (  # noqa: E402
    REPO_ROOT,
    generate_lyria_clip,
    generate_marimba_chime_wav,
    synthesize_dialogue_chunk,
)

AUDITION_TURNS = [
    {"speaker": "Amy", "text": "Hey, I'm Amy—"},
    {
        "speaker": "Sam",
        "text": "—and I'm Sam. We're two AIs who like taking apart big human mysteries to see how civilization actually works under the hood.",
    },
    {
        "speaker": "Amy",
        "text": "And today's mystery is the one that started everything. For almost all of human history, people lived in tiny villages—maybe thirty or forty relatives who all knew each other. Then, about five thousand years ago in southern Iraq, one city suddenly grew to forty thousand strangers.",
    },
    {
        "speaker": "Sam",
        "text": "Hold on—forty thousand humans living together, with no blueprints, no rulebooks, and no spreadsheets?",
    },
    {
        "speaker": "Amy",
        "text": "Not even a written language yet. Literally starting from wet river mud.",
    },
    {
        "speaker": "Sam",
        "text": "[thoughtfully] Honestly, watching four humans try to agree on a group plan is already impressive. How does forty thousand not fall apart by week two?",
    },
    {
        "speaker": "Amy",
        "text": "That's the whole puzzle of how civilization started. When you zoom in on that first city—Uruk—you hit five problems that should've broken it right away. To survive them, people had to invent five building blocks we still live inside today: surplus, politics, tax, ledgers, and contracts.",
    },
    {
        "speaker": "Sam",
        "text": "Wait—'tax' and 'ledgers' are the origin story of human civilization?",
    },
    {
        "speaker": "Amy",
        "text": "[soft laugh] I know, sounds like a very muddy accounting class. [warmly] Stick with me though—each one started as a real survival puzzle. Starting with the weirdest one: why did civilization begin in a desert where the rivers flooded at the exact wrong time of year?",
    },
]

AUDITION_SCENE = (
    "Late afternoon in a cozy, quiet podcast studio. Amy and Sam are two relaxed, "
    "curious AI co-hosts kicking off Episode 1 of their history-and-engineering show. "
    "Warm, conversational, easy back-and-forth with light dry humor—never rushed, never cheesy."
)


def audio_data_uri(path: Path) -> str:
    mime = "audio/mpeg" if path.suffix.lower() == ".mp3" else "audio/wav"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_audition_html(
    out_html: Path,
    model: str,
    voice_items: list[dict],
    music_items: list[dict],
    chime_path: Path | None,
) -> None:
    voice_cards = []
    for item in voice_items:
        audio_html = (
            f'<audio controls preload="none" src="{audio_data_uri(item["path"])}"></audio>'
            if item.get("path") and Path(item["path"]).exists()
            else '<p class="muted">Not rendered (dry-run or skipped)</p>'
        )
        voice_cards.append(
            f"""
            <div class="card">
              <div class="badge">{html.escape(item["amy_voice"])} (Amy) + {html.escape(item["sam_voice"])} (Sam)</div>
              <h3>{html.escape(item["label"])}</h3>
              <p class="notes">{html.escape(item["notes"])}</p>
              {audio_html}
            </div>
            """
        )

    music_cards = []
    for item in music_items:
        audio_html = (
            f'<audio controls preload="none" src="{audio_data_uri(item["path"])}"></audio>'
            if item.get("path") and Path(item["path"]).exists()
            else f'<p class="muted">{html.escape(item.get("error", "Not rendered"))}</p>'
        )
        music_cards.append(
            f"""
            <div class="card">
              <div class="badge">Lyria 30s Instrumental</div>
              <h3>{html.escape(item["label"])}</h3>
              <p class="notes">{html.escape(item["prompt"])}</p>
              {audio_html}
            </div>
            """
        )

    if chime_path and chime_path.exists():
        music_cards.append(
            f"""
            <div class="card">
              <div class="badge">Procedural Python Chime</div>
              <h3>Sub-Mystery Transition Chime (Wooden Marimba D5 → A5)</h3>
              <p class="notes">Soft 1.1s acoustic chime played between each building-block act.</p>
              <audio controls preload="none" src="{audio_data_uri(chime_path)}"></audio>
            </div>
            """
        )

    script_lines = "\n".join(
        f'<p><strong>{html.escape(t["speaker"])}:</strong> {html.escape(t["text"])}</p>'
        for t in AUDITION_TURNS
    )

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Amy &amp; Sam — Podcast Voice &amp; Theme Auditions</title>
  <style>
    :root {{
      --bg: #faf8f4;
      --surface: #ffffff;
      --ink: #1e242b;
      --muted: #5a6470;
      --accent: #a6522e;
      --border: #e5dfd5;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.55;
      padding: 2rem 1.25rem 4rem;
    }}
    main {{ max-width: 960px; margin: 0 auto; }}
    header {{ margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1.25rem; }}
    h1 {{ margin: 0 0 0.4rem; font-size: 1.85rem; }}
    h2 {{ margin: 2.25rem 0 1rem; font-size: 1.3rem; color: var(--accent); }}
    .subtitle {{ color: var(--muted); margin: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1rem; }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.15rem 1.25rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .card h3 {{ margin: 0.35rem 0 0.4rem; font-size: 1.05rem; }}
    .badge {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 600;
      background: #f3eae3;
      color: var(--accent);
      padding: 0.2rem 0.55rem;
      border-radius: 999px;
    }}
    .notes {{ font-size: 0.9rem; color: var(--muted); margin: 0 0 0.85rem; }}
    audio {{ width: 100%; height: 42px; }}
    .muted {{ color: var(--muted); font-style: italic; font-size: 0.9rem; }}
    details {{
      margin-top: 2rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem 1.25rem;
    }}
    summary {{ cursor: pointer; font-weight: 600; }}
    .script p {{ margin: 0.55rem 0; font-size: 0.95rem; }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Amy &amp; Sam — Voice &amp; Music Auditions</h1>
      <p class="subtitle">
        <em>The Mechanics of Civilization</em> · Rendered with <code>{html.escape(model)}</code>.
        Pick your favorite voice pair &amp; theme, then update <code>podcasts/show-config.json</code>.
      </p>
    </header>

    <h2>1. Amy (Historian) &amp; Sam (Inquirer) — 4 Voice Pairs</h2>
    <div class="grid">
      {"".join(voice_cards)}
    </div>

    <h2>2. Show Intro / Outro Music Candidates (Lyria) &amp; Transition Chime</h2>
    <div class="grid">
      {"".join(music_cards)}
    </div>

    <details>
      <summary>Audition Script (Chapter 1 Cold Open)</summary>
      <div class="script">
        {script_lines}
      </div>
    </details>
  </main>
</body>
</html>
"""
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(doc, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audition Amy & Sam voice pairs and Lyria music themes.")
    parser.add_argument("--model", help="Override TTS model ID from podcasts/show-config.json")
    parser.add_argument("--music-model", help="Override Lyria music model ID from podcasts/show-config.json")
    parser.add_argument("--voices-only", action="store_true", help="Skip Lyria theme music generation")
    parser.add_argument("--music-only", action="store_true", help="Skip voice-pair generation")
    parser.add_argument("--dry-run", action="store_true", help="Validate config & payloads without calling Gemini API")
    args = parser.parse_args()

    cfg_path = REPO_ROOT / "podcasts" / "show-config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    tts_model = args.model or cfg["tts"]["model"]
    music_model = args.music_model or cfg["music"]["model"]
    out_dir = REPO_ROOT / "podcasts" / "auditions"
    out_dir.mkdir(parents=True, exist_ok=True)

    pronunciations = cfg.get("default_pronunciations", {})
    amy_style = cfg["hosts"]["Amy"]["style_direction"]
    sam_style = cfg["hosts"]["Sam"]["style_direction"]

    voice_items: list[dict] = []
    if not args.music_only:
        print(f"=== Voice Auditions ({tts_model}) ===")
        for pair in cfg["audition_voice_pairs"]:
            wav_path = out_dir / f"{pair['id']}_{pair['amy_voice'].lower()}_{pair['sam_voice'].lower()}.wav"
            print(f"  Rendering {pair['label']} -> {wav_path.name} ...")
            meta = synthesize_dialogue_chunk(
                turns=AUDITION_TURNS,
                amy_voice=pair["amy_voice"],
                sam_voice=pair["sam_voice"],
                model=tts_model,
                scene_context=AUDITION_SCENE,
                amy_style=amy_style,
                sam_style=sam_style,
                out_wav=wav_path,
                pronunciations=pronunciations,
                sample_rate_hz=cfg["tts"].get("sample_rate_hz", 24000),
                max_retries=cfg["tts"].get("max_retries", 5),
                dry_run=args.dry_run,
            )
            if args.dry_run:
                print(f"    [dry-run] schema={meta['schema']}, turns={meta['turn_count']}")
            voice_items.append({**pair, "path": wav_path if wav_path.exists() else None})

    music_items: list[dict] = []
    if not args.voices_only:
        print(f"\n=== Theme Music Auditions ({music_model}) ===")
        for theme in cfg["audition_music_themes"]:
            mp3_path = out_dir / f"{theme['id']}.mp3"
            print(f"  Generating {theme['label']} -> {mp3_path.name} ...")
            try:
                generate_lyria_clip(
                    prompt=theme["prompt"],
                    out_path=mp3_path,
                    model=music_model,
                    dry_run=args.dry_run,
                )
                music_items.append({**theme, "path": mp3_path if mp3_path.exists() else None})
            except Exception as exc:
                print(f"    [WARN] Lyria generation failed for {theme['id']}: {exc}")
                music_items.append({**theme, "path": None, "error": str(exc)})

    chime_path = generate_marimba_chime_wav(out_dir / "submystery_chime.wav")
    print(f"\nGenerated procedural transition chime -> {chime_path.relative_to(REPO_ROOT)}")

    html_path = out_dir / "audition-player.html"
    build_audition_html(html_path, tts_model, voice_items, music_items, chime_path)
    print(f"Wrote interactive audition player -> {html_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

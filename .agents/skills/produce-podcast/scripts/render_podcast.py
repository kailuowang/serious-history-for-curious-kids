#!/usr/bin/env python3
"""Render a full chapter podcast episode from podcasts/<ch>-script.json (or .md)
using Gemini native 2-speaker TTS + ffmpeg mastering (-16 LUFS + MP3 chapters + QA).

Usage:
    python3 .agents/skills/produce-podcast/scripts/render_podcast.py ch01
    python3 .agents/skills/produce-podcast/scripts/render_podcast.py ch01 --from-md
    python3 .agents/skills/produce-podcast/scripts/render_podcast.py ch01 --only-act 2
    python3 .agents/skills/produce-podcast/scripts/render_podcast.py ch01 --model gemini-3.8-flash-tts
    python3 .agents/skills/produce-podcast/scripts/render_podcast.py ch01 --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _tts_core import (  # noqa: E402
    REPO_ROOT,
    generate_marimba_chime_wav,
    synthesize_dialogue_chunk,
)

ACT_RE = re.compile(r"^##\s+(.+)$")
TURN_RE = re.compile(r"^\*\*(Amy|Sam):\*\*\s*(.+)$")


def parse_script_md(md_path: Path, chapter_id: str, default_pronunciations: dict[str, str]) -> dict[str, Any]:
    """Convert podcasts/<ch>-script.md into the canonical cue-sheet JSON structure."""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    title = f"Episode {chapter_id}"
    acts: list[dict[str, Any]] = []
    current_act: dict[str, Any] | None = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and title == f"Episode {chapter_id}":
            title = line[2:].strip()
            continue
        act_m = ACT_RE.match(line)
        if act_m:
            act_title = act_m.group(1).strip()
            current_act = {
                "act_index": len(acts),
                "title": act_title,
                "play_chime_before": len(acts) > 0,
                "scene_context": (
                    f"Cozy podcast studio. Amy and Sam are recording '{act_title}' "
                    "in a relaxed, curious, conversational back-and-forth with crisp timing."
                ),
                "turns": [],
            }
            acts.append(current_act)
            continue
        turn_m = TURN_RE.match(line)
        if turn_m:
            if current_act is None:
                current_act = {
                    "act_index": 0,
                    "title": "Cold Open",
                    "play_chime_before": False,
                    "scene_context": "Cozy podcast studio, warm and conversational.",
                    "turns": [],
                }
                acts.append(current_act)
            current_act["turns"].append(
                {
                    "speaker": turn_m.group(1),
                    "text": turn_m.group(2).strip(),
                }
            )

    return {
        "chapter_id": chapter_id,
        "episode_title": title,
        "pronunciations": dict(default_pronunciations),
        "acts": acts,
    }


def wav_duration_sec(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def make_silence_wav(out_wav: Path, duration_ms: int, sample_rate: int = 24000) -> Path:
    n_frames = int(sample_rate * (duration_ms / 1000.0))
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)
    return out_wav


def run_ffmpeg(cmd: list[str], capture_stderr: bool = False) -> subprocess.CompletedProcess[str]:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg is not installed or not on PATH. Install it (e.g., 'brew install ffmpeg' or 'sudo apt-get install ffmpeg')."
        )
    return subprocess.run(
        cmd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE if capture_stderr else None,
    )


def build_ffmetadata(
    show_title: str,
    episode_title: str,
    chapter_markers: list[tuple[int, int, str]],
    out_path: Path,
) -> Path:
    def esc(val: str) -> str:
        return val.replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;").replace("#", "\\#").replace("\n", " ")

    lines = [
        ";FFMETADATA1",
        f"title={esc(episode_title)}",
        f"artist={esc('Amy & Sam')}",
        f"album={esc(show_title)}",
        "genre=Podcast",
        "",
    ]
    for start_ms, end_ms, title in chapter_markers:
        lines.extend(
            [
                "[CHAPTER]",
                "TIMEBASE=1/1000",
                f"START={start_ms}",
                f"END={end_ms}",
                f"title={esc(title)}",
                "",
            ]
        )
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def run_audio_qa(mp3_path: Path) -> None:
    print("\n=== Pass 6: Automated Audio QA ===")
    res = run_ffmpeg(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(mp3_path),
            "-af",
            "volumedetect,silencedetect=noise=-42dB:d=2.5",
            "-f",
            "null",
            "-",
        ],
        capture_stderr=True,
    )
    stderr = res.stderr or ""
    mean_v = re.search(r"mean_volume:\s*([-\d.]+ dB)", stderr)
    max_v = re.search(r"max_volume:\s*([-\d.]+ dB)", stderr)
    dur_m = re.search(r"Duration:\s*([\d:.]+)", stderr)
    silences = re.findall(r"silence_duration:\s*([\d.]+)", stderr)

    print(f"  File:            {mp3_path.relative_to(REPO_ROOT)}")
    print(f"  Duration:        {dur_m.group(1) if dur_m else 'unknown'}")
    print(f"  Mean volume:     {mean_v.group(1) if mean_v else 'unknown'}")
    print(f"  Peak volume:     {max_v.group(1) if max_v else 'unknown'}")
    if silences:
        print(f"  [WARN] Found {len(silences)} silence(s) > 2.5s: {', '.join(s + 's' for s in silences)}")
    else:
        print("  Dead-air check:  PASS (zero unexpected silences > 2.5s)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthesize and master a chapter podcast episode.")
    parser.add_argument("chapter_id", help="Chapter ID, e.g. ch01")
    parser.add_argument("--from-md", action="store_true", help="Compile script JSON from podcasts/<ch>-script.md first")
    parser.add_argument("--only-act", type=int, default=None, help="Re-render only a single act index (0-based), then remaster")
    parser.add_argument("--force", action="store_true", help="Re-synthesize all acts even if cached WAVs exist")
    parser.add_argument("--model", help="Override TTS model ID from podcasts/show-config.json")
    parser.add_argument("--dry-run", action="store_true", help="Validate script & payloads without calling Gemini API or ffmpeg")
    args = parser.parse_args()

    ch = args.chapter_id
    cfg = json.loads((REPO_ROOT / "podcasts" / "show-config.json").read_text(encoding="utf-8"))
    tts_model = args.model or cfg["tts"]["model"]
    sample_rate = int(cfg["tts"].get("sample_rate_hz", 24000))
    master_cfg = cfg.get("audio_mastering", {})

    script_json_path = REPO_ROOT / "podcasts" / f"{ch}-script.json"
    script_md_path = REPO_ROOT / "podcasts" / f"{ch}-script.md"

    if args.from_md or not script_json_path.exists():
        if not script_md_path.exists():
            raise FileNotFoundError(f"Neither {script_json_path} nor {script_md_path} exists.")
        cue = parse_script_md(script_md_path, ch, cfg.get("default_pronunciations", {}))
        script_json_path.write_text(json.dumps(cue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Compiled cue sheet -> {script_json_path.relative_to(REPO_ROOT)}")
    else:
        cue = json.loads(script_json_path.read_text(encoding="utf-8"))

    amy_voice = cfg["hosts"]["Amy"]["voice_name"]
    sam_voice = cfg["hosts"]["Sam"]["voice_name"]
    amy_style = cfg["hosts"]["Amy"]["style_direction"]
    sam_style = cfg["hosts"]["Sam"]["style_direction"]
    pronunciations = {**cfg.get("default_pronunciations", {}), **cue.get("pronunciations", {})}

    tmp_dir = REPO_ROOT / "podcasts" / "tmp" / ch
    tmp_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Rendering {ch}: {cue.get('episode_title', ch)} ({tts_model}) ===")
    print(f"Voices: Amy={amy_voice}, Sam={sam_voice}")

    act_wavs: list[tuple[dict[str, Any], Path]] = []
    for idx, act in enumerate(cue["acts"]):
        out_wav = tmp_dir / f"act_{idx:02d}.wav"
        should_render = args.dry_run or args.force or (args.only_act == idx) or (args.only_act is None and not out_wav.exists())
        if should_render:
            print(f"  Act {idx:02d} ({act['title']}) — {len(act['turns'])} turns -> {out_wav.name}")
            meta = synthesize_dialogue_chunk(
                turns=act["turns"],
                amy_voice=amy_voice,
                sam_voice=sam_voice,
                model=tts_model,
                scene_context=act.get("scene_context", "Cozy podcast studio, warm conversational back-and-forth."),
                amy_style=amy_style,
                sam_style=sam_style,
                out_wav=out_wav,
                pronunciations=pronunciations,
                sample_rate_hz=sample_rate,
                max_retries=int(cfg["tts"].get("max_retries", 5)),
                dry_run=args.dry_run,
            )
            if args.dry_run:
                print(f"    [dry-run] schema={meta['schema']}, turns={meta['turn_count']}")
        else:
            print(f"  Act {idx:02d} ({act['title']}) — using cached {out_wav.name}")
        act_wavs.append((act, out_wav))

    if args.dry_run:
        print("\n[dry-run] Complete. No API calls or ffmpeg commands executed.")
        return 0

    # Build timeline with optional intro/outro music + subtle wooden marimba chimes
    use_chimes = bool(cfg.get("music", {}).get("use_submystery_chimes", True))
    chime_wav = generate_marimba_chime_wav(tmp_dir / "chime.wav", sample_rate=sample_rate) if use_chimes else None
    gap_before = make_silence_wav(tmp_dir / "gap_before.wav", int(master_cfg.get("chime_gap_before_ms", 350)), sample_rate)
    gap_after = make_silence_wav(tmp_dir / "gap_after.wav", int(master_cfg.get("chime_gap_after_ms", 450)), sample_rate)
    act_gap = make_silence_wav(tmp_dir / "act_gap.wav", int(master_cfg.get("act_gap_ms", 650)), sample_rate)

    segments: list[Path] = []
    chapter_markers: list[tuple[int, int, str]] = []
    cursor_ms = 0

    # Optional Lyria intro sting
    intro_rel = cfg.get("music", {}).get("intro_track")
    intro_src = (REPO_ROOT / intro_rel) if intro_rel else None
    if intro_src and intro_src.is_file():
        intro_dur = float(cfg["music"].get("intro_duration_sec", 7.0))
        intro_wav = tmp_dir / "intro_trimmed.wav"
        fade_start = max(0.5, intro_dur - 1.8)
        run_ffmpeg(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(intro_src),
                "-t", f"{intro_dur:.2f}",
                "-af", f"afade=t=in:st=0:d=0.4,afade=t=out:st={fade_start:.2f}:d=1.8,volume=0.55",
                "-ac", "1", "-ar", str(sample_rate), "-c:a", "pcm_s16le",
                str(intro_wav),
            ]
        )
        segments.append(intro_wav)
        cursor_ms += int(round(wav_duration_sec(intro_wav) * 1000))

    # Voice acts + chimes
    for idx, (act, wav_path) in enumerate(act_wavs):
        if idx > 0:
            if use_chimes and act.get("play_chime_before", True) and chime_wav is not None:
                for seg in (gap_before, chime_wav, gap_after):
                    segments.append(seg)
                    cursor_ms += int(round(wav_duration_sec(seg) * 1000))
            else:
                segments.append(act_gap)
                cursor_ms += int(round(wav_duration_sec(act_gap) * 1000))

        act_dur_ms = int(round(wav_duration_sec(wav_path) * 1000))
        chapter_markers.append((cursor_ms, cursor_ms + act_dur_ms, act["title"]))
        segments.append(wav_path)
        cursor_ms += act_dur_ms

        word_count = sum(len(t["text"].split()) for t in act["turns"])
        wpm = word_count / max(act_dur_ms / 60000.0, 0.01)
        if wpm < 95 or wpm > 230:
            print(f"  [QA WARN] Act {idx:02d} speech rate looks unusual ({wpm:.0f} wpm; check for skipped text or leaked directions).")

    # Optional Lyria outro sting
    outro_rel = cfg.get("music", {}).get("outro_track")
    outro_src = (REPO_ROOT / outro_rel) if outro_rel else None
    if outro_src and outro_src.is_file():
        outro_dur = float(cfg["music"].get("outro_duration_sec", 8.0))
        outro_wav = tmp_dir / "outro_trimmed.wav"
        fade_start = max(0.5, outro_dur - 2.5)
        run_ffmpeg(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(outro_src),
                "-t", f"{outro_dur:.2f}",
                "-af", f"afade=t=in:st=0:d=1.0,afade=t=out:st={fade_start:.2f}:d=2.5,volume=0.55",
                "-ac", "1", "-ar", str(sample_rate), "-c:a", "pcm_s16le",
                str(outro_wav),
            ]
        )
        segments.append(act_gap)
        segments.append(outro_wav)

    # Concatenate WAV segments via ffmpeg concat demuxer
    concat_list = tmp_dir / "concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{seg.resolve()}'" for seg in segments) + "\n",
        encoding="utf-8",
    )
    stitched_wav = tmp_dir / "stitched.wav"
    run_ffmpeg(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-ac", "1", "-ar", str(sample_rate), "-c:a", "pcm_s16le",
            str(stitched_wav),
        ]
    )

    # Write chapter metadata & master to -16 LUFS MP3
    meta_file = build_ffmetadata(
        show_title=cfg.get("show_title", "The Mechanics of Civilization"),
        episode_title=cue.get("episode_title", f"Episode {ch}"),
        chapter_markers=chapter_markers,
        out_path=tmp_dir / "chapters.ffmeta",
    )
    target_lufs = float(master_cfg.get("target_lufs", -16.0))
    true_peak = float(master_cfg.get("true_peak_db", -1.5))
    bitrate = str(master_cfg.get("mp3_bitrate", "128k"))
    out_mp3 = REPO_ROOT / "podcasts" / f"{ch}-episode.mp3"

    run_ffmpeg(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(stitched_wav),
            "-i", str(meta_file),
            "-map_metadata", "1",
            "-map_chapters", "1",
            "-af", f"loudnorm=I={target_lufs}:TP={true_peak}:LRA=11",
            "-c:a", "libmp3lame", "-b:a", bitrate,
            "-id3v2_version", "3",
            str(out_mp3),
        ]
    )

    run_audio_qa(out_mp3)
    print(f"\nDone! Mastered episode written to {out_mp3.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

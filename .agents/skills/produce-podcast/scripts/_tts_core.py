#!/usr/bin/env python3
"""Shared Gemini TTS (3.1 & 3.8), Lyria music, and pure-Python audio utilities."""

from __future__ import annotations

import base64
import math
import os
import re
import struct
import time
import wave
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

# Map inline square-bracket tags (script canonical format) for Gemini 3.8
TAG_TO_38_VOCAL = {
    "soft laugh": "<laugh>",
    "sighs": "<sigh>",
    "short pause": "<short pause>",
}
STYLE_ONLY_TAGS = {"warmly", "thoughtfully", "gently", "cheerfully"}
TAG_RE = re.compile(r"\[([^\]]+)\]")


def load_gemini_api_key() -> str | None:
    """Resolve GEMINI_API_KEY from env or local/cloud .env files without logging it."""
    for env_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(env_name, "").strip()
        if val:
            return val

    candidate_files: list[Path] = [
        REPO_ROOT / ".env",
        REPO_ROOT / ".env.local",
        Path.home() / ".gemini.env",
        Path.home() / ".env",
    ]
    upload_dir = Path("/home/antigravity/upload")
    if upload_dir.is_dir():
        candidate_files.extend(sorted(upload_dir.glob("*.env")))

    for path in candidate_files:
        if not path.is_file():
            continue
        try:
            for raw in path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                if line.startswith("export "):
                    line = line[len("export ") :].strip()
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                    return v
        except OSError:
            continue
    return None


def make_genai_client():
    """Instantiate google.genai.Client lazily so --dry-run works without SDK."""
    api_key = load_gemini_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Set GEMINI_API_KEY in your environment, "
            "or place GEMINI_API_KEY=... in .env or ~/.gemini.env."
        )
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            'google-genai SDK is not installed. Run: pip install --upgrade "google-genai>=2.25.0"'
        ) from exc
    return genai.Client(api_key=api_key, http_options={"api_version": "v1beta"})


def apply_pronunciations(text: str, pronunciations: dict[str, str] | None) -> str:
    """Apply whole-word phonetic substitutions for TTS clarity."""
    if not pronunciations:
        return text
    out = text
    for term, spoken in sorted(pronunciations.items(), key=lambda kv: -len(kv[0])):
        if not term or not spoken:
            continue
        out = re.sub(rf"\b{re.escape(term)}\b", spoken, out)
    return out


def build_31_prompt(
    turns: list[dict[str, Any]],
    scene_context: str,
    amy_style: str,
    sam_style: str,
    pronunciations: dict[str, str] | None = None,
) -> str:
    """Build a LiveKit-verified prompt for legacy gemini-3.1-flash-tts-preview."""
    transcript_lines: list[str] = []
    for turn in turns:
        speaker = turn["speaker"]
        raw_text = turn.get("tts_text") or apply_pronunciations(turn["text"], pronunciations)
        transcript_lines.append(f"{speaker}: {raw_text.strip()}")

    return (
        "Synthesize speech for the performance defined below. The profile, scene,\n"
        "performance notes, and context are direction only. Do NOT speak them.\n"
        "Speak ONLY the lines under #### TRANSCRIPT.\n\n"
        "# AUDIO PROFILE: Amy and Sam\n"
        "## Two curious, chill AI podcast co-hosts unpacking human history\n\n"
        "## SCENE: Cozy podcast studio\n"
        f"{scene_context.strip()}\n\n"
        "### PERFORMANCE\n"
        f"Style: Amy — {amy_style.strip()} Sam — {sam_style.strip()}\n"
        "Pace: Natural, conversational, unhurried back-and-forth with crisp timing on dry jokes and thoughtful beats after big clues.\n"
        "Accent: Natural American English.\n\n"
        "### CONTEXT\n"
        "Amy and Sam are two candid, sharp AIs hosting a history-and-engineering mystery podcast for curious listeners. "
        "They talk like relaxed intellectual peers, never cheesy or lecturing.\n\n"
        "#### TRANSCRIPT\n"
        + "\n".join(transcript_lines)
        + "\n"
    )


def build_38_interaction_input(
    turns: list[dict[str, Any]],
    amy_style: str,
    sam_style: str,
    pronunciations: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Build Interactions API user_input content blocks for gemini-3.8-flash-tts."""
    content_blocks: list[dict[str, Any]] = []
    base_styles = {"Amy": amy_style.strip(), "Sam": sam_style.strip()}

    for turn in turns:
        speaker = turn["speaker"]
        raw_text = turn.get("tts_text") or apply_pronunciations(turn["text"], pronunciations)
        extra_styles: list[str] = []

        def _replace_tag(match: re.Match[str]) -> str:
            tag = match.group(1).strip().lower()
            if tag in TAG_TO_38_VOCAL:
                return TAG_TO_38_VOCAL[tag]
            if tag in STYLE_ONLY_TAGS:
                extra_styles.append(tag)
                return ""
            return ""

        cleaned = re.sub(r"\s{2,}", " ", TAG_RE.sub(_replace_tag, raw_text)).strip()
        # Keep Gemini 3.8 speech_metadata.style short to preserve long-form voice stability.
        style_parts = [s for s in [turn.get("delivery_note") or base_styles.get(speaker, ""), *dict.fromkeys(extra_styles)] if s]
        annotation: dict[str, Any] = {
            "type": "speech_metadata",
            "speaker": speaker,
        }
        if style_parts:
            annotation["style"] = ", ".join(style_parts)

        content_blocks.append(
            {
                "type": "text",
                "text": cleaned,
                "annotations": [annotation],
            }
        )

    return [{"type": "user_input", "content": content_blocks}]


def write_audio_as_wav(audio_bytes: bytes, out_wav: Path, sample_rate_hz: int = 24000) -> None:
    """Save either complete WAV bytes (3.8) or raw 16-bit mono PCM (3.1) as a valid WAV."""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    if audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE":
        out_wav.write_bytes(audio_bytes)
        return
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(sample_rate_hz)
        wf.writeframes(audio_bytes)


def extract_interaction_audio(interaction: Any) -> tuple[bytes, str]:
    """Extract audio bytes + mime_type from a Gemini Interactions API response (TTS 3.8 or Lyria)."""
    audio_data: str | bytes | None = None
    mime_type = "audio/wav"

    out_audio = getattr(interaction, "output_audio", None)
    if out_audio is not None and getattr(out_audio, "data", None):
        audio_data = out_audio.data
        mime_type = getattr(out_audio, "mime_type", None) or mime_type

    if audio_data is None:
        for container_attr in ("outputs", "steps"):
            items = getattr(interaction, container_attr, None) or []
            for item in items:
                blocks = getattr(item, "content", None) or getattr(item, "outputs", None) or [item]
                if not isinstance(blocks, list):
                    blocks = [blocks]
                for blk in blocks:
                    btype = str(getattr(blk, "type", "") or "").lower()
                    bmime = str(getattr(blk, "mime_type", "") or "").lower()
                    bdata = getattr(blk, "data", None)
                    if bdata and ("audio" in btype or "audio" in bmime):
                        audio_data = bdata
                        mime_type = getattr(blk, "mime_type", None) or mime_type

    if audio_data is None:
        raise ValueError("Gemini Interactions API response contained no audio block.")

    raw = base64.b64decode(audio_data) if isinstance(audio_data, str) else bytes(audio_data)
    return raw, mime_type


def extract_generate_content_audio(response: Any) -> bytes:
    """Extract inline audio bytes from a legacy Gemini generate_content TTS response."""
    candidates = getattr(response, "candidates", None) or []
    for cand in candidates:
        content = getattr(cand, "content", None)
        parts = getattr(content, "parts", None) or []
        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline is not None and getattr(inline, "data", None):
                data = inline.data
                if isinstance(data, str):
                    return base64.b64decode(data)
                return bytes(data)
    raise ValueError("Gemini TTS response contained no audio inline_data (preview empty-part glitch).")


def synthesize_dialogue_chunk(
    *,
    turns: list[dict[str, Any]],
    amy_voice: str,
    sam_voice: str,
    model: str,
    scene_context: str,
    amy_style: str,
    sam_style: str,
    out_wav: Path,
    pronunciations: dict[str, str] | None = None,
    sample_rate_hz: int = 24000,
    max_retries: int = 5,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Synthesize a multi-speaker Amy & Sam dialogue chunk to WAV."""
    is_38 = "3.8" in model
    if is_38:
        payload: Any = build_38_interaction_input(turns, amy_style, sam_style, pronunciations)
    else:
        payload = build_31_prompt(turns, scene_context, amy_style, sam_style, pronunciations)

    meta = {
        "model": model,
        "schema": "gemini-3.8-interactions" if is_38 else "gemini-3.1-transcript",
        "amy_voice": amy_voice,
        "sam_voice": sam_voice,
        "turn_count": len(turns),
        "out_wav": str(out_wav),
    }
    if dry_run:
        meta["payload_preview"] = (
            payload[:500] if isinstance(payload, str) else payload[0]["content"][:2]
        )
        return meta

    client = make_genai_client()
    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            if is_38:
                interaction = client.interactions.create(
                    model=model,
                    input=payload,
                    response_format={"type": "audio"},
                    generation_config={
                        "speech_config": [
                            {"speaker": "Amy", "voice": amy_voice},
                            {"speaker": "Sam", "voice": sam_voice},
                        ]
                    },
                )
                audio_bytes, _ = extract_interaction_audio(interaction)
            else:
                from google.genai import types

                speech_cfg = types.SpeechConfig(
                    multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=[
                            types.SpeakerVoiceConfig(
                                speaker="Amy",
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=amy_voice)
                                ),
                            ),
                            types.SpeakerVoiceConfig(
                                speaker="Sam",
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=sam_voice)
                                ),
                            ),
                        ]
                    )
                )
                gen_cfg = types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=speech_cfg,
                )
                response = client.models.generate_content(
                    model=model,
                    contents=payload,
                    config=gen_cfg,
                )
                audio_bytes = extract_generate_content_audio(response)

            write_audio_as_wav(audio_bytes, out_wav, sample_rate_hz=sample_rate_hz)
            meta["bytes"] = len(audio_bytes)
            return meta
        except Exception as exc:
            last_err = exc
            if attempt < max_retries:
                sleep_s = min(2.0 * (2 ** (attempt - 1)), 20.0)
                print(f"    [retry {attempt}/{max_retries}] {exc} — waiting {sleep_s:.1f}s...")
                time.sleep(sleep_s)
    raise RuntimeError(f"Gemini TTS failed after {max_retries} attempts: {last_err}") from last_err


def generate_lyria_clip(
    *,
    prompt: str,
    out_path: Path,
    model: str = "lyria-3-clip-preview",
    dry_run: bool = False,
) -> dict[str, Any]:
    """Generate a 30-second instrumental music clip with Lyria via Gemini Interactions API."""
    meta = {"model": model, "out_path": str(out_path), "prompt": prompt}
    if dry_run:
        return meta

    client = make_genai_client()
    interaction = client.interactions.create(
        model=model,
        input=prompt,
    )
    raw, mime_type = extract_interaction_audio(interaction)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    meta["bytes"] = len(raw)
    meta["mime_type"] = mime_type
    return meta


def generate_marimba_chime_wav(out_wav: Path, sample_rate: int = 24000) -> Path:
    """Generate a subtle, warm 2-note wooden marimba sub-mystery chime (pure Python)."""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    duration = 1.15
    total_samples = int(sample_rate * duration)
    notes = [
        (0.00, 587.33, 0.24),  # D5
        (0.17, 880.00, 0.26),  # A5 (open warm fifth)
    ]
    buf = [0.0] * total_samples
    for start_s, freq, amp in notes:
        start_i = int(start_s * sample_rate)
        for i in range(start_i, total_samples):
            t = (i - start_i) / sample_rate
            attack = min(1.0, t / 0.008)
            # Warm wooden bar: fundamental + gentle 4x harmonic that decays quickly
            env_fund = math.exp(-t * 4.4)
            env_wood = math.exp(-t * 18.0)
            sample = (
                amp
                * attack
                * (0.82 * env_fund * math.sin(2.0 * math.pi * freq * t)
                   + 0.18 * env_wood * math.sin(2.0 * math.pi * (freq * 3.98) * t))
            )
            buf[i] += sample

    # Gentle fade out tail
    fade_len = int(0.08 * sample_rate)
    for k in range(fade_len):
        idx = total_samples - 1 - k
        buf[idx] *= k / fade_len

    pcm = bytearray()
    for val in buf:
        clamped = max(-0.95, min(0.95, val))
        pcm.extend(struct.pack("<h", int(clamped * 32767)))

    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(bytes(pcm))
    return out_wav

"""Bounded Chinese-LiPS subset preparation for the P0-A R1 smoke test."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from huggingface_hub import HfFileSystem

from video_evidence_agent.audio import probe_media_duration_ms


class ChineseLipsPreparationError(RuntimeError):
    """Raised when the bounded dataset preparation cannot fail closed."""


@dataclass(frozen=True)
class ChineseLipsClip:
    clip_id: str
    speaker: str
    topic: str
    wav_path: str
    ppt_path: str
    face_path: str
    gt_text: str

    @property
    def numeric_suffix(self) -> int:
        try:
            return int(self.clip_id.rsplit("_", 1)[1])
        except (IndexError, ValueError) as exc:
            raise ChineseLipsPreparationError(
                f"clip ID has no numeric suffix: {self.clip_id}"
            ) from exc

    def to_dict(self) -> dict[str, object]:
        return {
            "clip_id": self.clip_id,
            "speaker": self.speaker,
            "topic": self.topic,
            "wav_path": self.wav_path,
            "ppt_path": self.ppt_path,
            "face_path": self.face_path,
            "gt_text": self.gt_text,
        }


@dataclass(frozen=True)
class ArchiveSelection:
    members: tuple[zipfile.ZipInfo, ...]
    compressed_bytes: int
    uncompressed_bytes: int


REQUIRED_METADATA_FIELDS = {"ID", "TOPIC", "WAV", "PPT", "FACE", "TEXT"}


def _speaker_from_clip_id(clip_id: str) -> str:
    try:
        speaker, suffix = clip_id.rsplit("_", 1)
        int(suffix)
    except (ValueError, TypeError) as exc:
        raise ChineseLipsPreparationError(f"invalid Chinese-LiPS clip ID: {clip_id}") from exc
    if not speaker:
        raise ChineseLipsPreparationError(f"invalid Chinese-LiPS clip ID: {clip_id}")
    return speaker


def select_clips(
    metadata_path: Path,
    *,
    topic: str,
    count: int,
    speaker: str | None = None,
) -> list[ChineseLipsClip]:
    """Choose clips by split metadata only, never by transcript content."""

    if count <= 0:
        raise ChineseLipsPreparationError("clip count must be positive")
    if not metadata_path.is_file():
        raise ChineseLipsPreparationError(f"metadata file does not exist: {metadata_path}")

    with metadata_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not REQUIRED_METADATA_FIELDS.issubset(reader.fieldnames):
            raise ChineseLipsPreparationError("metadata is missing required Chinese-LiPS fields")
        grouped: dict[str, list[ChineseLipsClip]] = defaultdict(list)
        seen_ids: set[str] = set()
        for row in reader:
            if row["TOPIC"] != topic:
                continue
            clip_id = row["ID"].strip()
            if clip_id in seen_ids:
                raise ChineseLipsPreparationError(f"duplicate clip ID in metadata: {clip_id}")
            seen_ids.add(clip_id)
            clip_speaker = _speaker_from_clip_id(clip_id)
            text = row["TEXT"].strip()
            if not text:
                raise ChineseLipsPreparationError(f"clip has empty ground-truth text: {clip_id}")
            grouped[clip_speaker].append(
                ChineseLipsClip(
                    clip_id=clip_id,
                    speaker=clip_speaker,
                    topic=topic,
                    wav_path=row["WAV"].strip(),
                    ppt_path=row["PPT"].strip(),
                    face_path=row["FACE"].strip(),
                    gt_text=text,
                )
            )

    if speaker is not None:
        candidates = grouped.get(speaker, [])
        if len(candidates) < count:
            raise ChineseLipsPreparationError(
                f"requested speaker has {len(candidates)} {topic} clips, needs {count}"
            )
        selected_speaker = speaker
    else:
        eligible = sorted(
            ((candidate_speaker, len(clips)) for candidate_speaker, clips in grouped.items()),
            key=lambda item: (-item[1], item[0]),
        )
        if not eligible or eligible[0][1] < count:
            raise ChineseLipsPreparationError(
                f"no {topic} speaker has at least {count} validation clips"
            )
        selected_speaker = eligible[0][0]

    ordered = sorted(grouped[selected_speaker], key=lambda clip: clip.numeric_suffix)
    selected = ordered[:count]
    suffixes = [clip.numeric_suffix for clip in selected]
    expected = list(range(suffixes[0], suffixes[0] + count))
    if suffixes != expected:
        raise ChineseLipsPreparationError("selected clip IDs are not a consecutive sequence")
    return selected


def processed_member_names(clips: list[ChineseLipsClip]) -> set[str]:
    return {
        f"processed_val/{clip.clip_id}{suffix}"
        for clip in clips
        for suffix in (".wav", ".mp4")
    }


def inspect_archive_members(
    archive: zipfile.ZipFile,
    wanted_names: set[str],
    *,
    max_compressed_bytes: int,
) -> ArchiveSelection:
    """Validate exact members and budget before reading any selected payload."""

    if max_compressed_bytes <= 0:
        raise ChineseLipsPreparationError("compressed-byte budget must be positive")
    infos = {info.filename: info for info in archive.infolist()}
    missing = sorted(wanted_names - infos.keys())
    if missing:
        raise ChineseLipsPreparationError(f"processed archive is missing {len(missing)} entries")

    selected = tuple(infos[name] for name in sorted(wanted_names))
    for info in selected:
        path = PurePosixPath(info.filename)
        if path.is_absolute() or ".." in path.parts or info.is_dir():
            raise ChineseLipsPreparationError(f"unsafe archive member: {info.filename}")

    compressed_bytes = sum(info.compress_size for info in selected)
    if compressed_bytes > max_compressed_bytes:
        raise ChineseLipsPreparationError(
            f"selected archive entries need {compressed_bytes} compressed bytes, "
            f"budget is {max_compressed_bytes}"
        )
    return ArchiveSelection(
        members=selected,
        compressed_bytes=compressed_bytes,
        uncompressed_bytes=sum(info.file_size for info in selected),
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(f"{path.name}.partial")
    partial.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    partial.replace(path)


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(f"{path.name}.partial")
    with partial.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")
    partial.replace(path)


def _copy_member(archive: zipfile.ZipFile, info: zipfile.ZipInfo, destination: Path) -> None:
    partial = destination.with_name(f"{destination.name}.partial")
    partial.parent.mkdir(parents=True, exist_ok=True)
    partial.unlink(missing_ok=True)
    with archive.open(info) as source, partial.open("wb") as target:
        shutil.copyfileobj(source, target, length=1024 * 1024)
    if partial.stat().st_size != info.file_size:
        partial.unlink(missing_ok=True)
        raise ChineseLipsPreparationError(f"extracted size mismatch: {info.filename}")
    partial.replace(destination)


def _require_binary(name: str) -> str:
    binary = shutil.which(name)
    if binary is None:
        raise ChineseLipsPreparationError(f"{name} is not available on PATH")
    return binary


def _run_ffmpeg(command: list[str], partial_path: Path, *, stage: str) -> None:
    partial_path.unlink(missing_ok=True)
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        partial_path.unlink(missing_ok=True)
        raise ChineseLipsPreparationError(
            f"ffmpeg {stage} failed with exit code {completed.returncode}"
        )


def _compose_clips(
    clips: list[ChineseLipsClip],
    extracted_dir: Path,
    output_path: Path,
) -> tuple[int, list[int]]:
    """Concatenate all clips while encoding audio only once to avoid AAC drift."""

    if not clips:
        raise ChineseLipsPreparationError("at least one clip is required")
    ffmpeg = _require_binary("ffmpeg")
    inputs: list[str] = []
    filters: list[str] = []
    concat_inputs: list[str] = []
    durations_ms: list[int] = []
    for index, clip in enumerate(clips):
        video_path = extracted_dir / f"{clip.clip_id}.mp4"
        audio_path = extracted_dir / f"{clip.clip_id}.wav"
        if not video_path.is_file() or not audio_path.is_file():
            raise ChineseLipsPreparationError(f"extracted media is missing for {clip.clip_id}")
        duration_ms = min(
            probe_media_duration_ms(video_path),
            probe_media_duration_ms(audio_path),
        )
        if duration_ms <= 0:
            raise ChineseLipsPreparationError(f"clip has no shared duration: {clip.clip_id}")
        durations_ms.append(duration_ms)
        duration_seconds = duration_ms / 1000
        video_input = index * 2
        audio_input = video_input + 1
        inputs.extend(["-i", str(video_path), "-i", str(audio_path)])
        filters.extend(
            [
                f"[{video_input}:v:0]fps=25,scale=96:96,format=yuv420p,"
                f"trim=duration={duration_seconds:.3f},setpts=PTS-STARTPTS[v{index}]",
                f"[{audio_input}:a:0]aformat=sample_rates=16000:channel_layouts=mono,"
                f"atrim=duration={duration_seconds:.3f},asetpts=PTS-STARTPTS[a{index}]",
            ]
        )
        concat_inputs.extend([f"[v{index}]", f"[a{index}]"])

    filters.append(
        "".join(concat_inputs)
        + f"concat=n={len(clips)}:v=1:a=1[composite_video][composite_audio]"
    )
    partial = output_path.with_name(f"{output_path.stem}.partial{output_path.suffix}")
    command = [
        ffmpeg,
        "-nostdin",
        "-y",
        *inputs,
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[composite_video]",
        "-map",
        "[composite_audio]",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-c:a",
        "aac",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-movflags",
        "+faststart",
        str(partial),
    ]
    _run_ffmpeg(command, partial, stage="single-pass composite concat")
    duration_ms = probe_media_duration_ms(partial)
    partial.replace(output_path)
    return duration_ms, durations_ms


def _reuse_extracted_selection(
    *,
    artifact_root: Path,
    clips: list[ChineseLipsClip],
    repo_id: str,
    revision: str,
    archive_filename: str,
    topic: str,
    max_compressed_bytes: int,
) -> ArchiveSelection:
    selection_path = artifact_root / "source" / "selected-clips.json"
    try:
        payload = json.loads(selection_path.read_text(encoding="utf-8"))
        selected_ids = [str(row["clip_id"]) for row in payload["clips"]]
        compressed_bytes = int(payload["compressed_bytes"])
        uncompressed_bytes = int(payload["uncompressed_bytes"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ChineseLipsPreparationError("cannot validate reusable extracted media") from exc
    expected = {
        "dataset_repo": repo_id,
        "dataset_revision": revision,
        "archive": archive_filename,
        "topic": topic,
        "speaker": clips[0].speaker,
        "clip_count": len(clips),
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        raise ChineseLipsPreparationError("reusable extraction provenance does not match request")
    if selected_ids != [clip.clip_id for clip in clips]:
        raise ChineseLipsPreparationError("reusable extraction clip IDs do not match selection")
    if compressed_bytes > max_compressed_bytes:
        raise ChineseLipsPreparationError("reusable extraction exceeds compressed-byte budget")

    extracted_dir = artifact_root / "source" / "extracted"
    media_paths = [
        extracted_dir / PurePosixPath(name).name
        for name in sorted(processed_member_names(clips))
    ]
    if any(not path.is_file() or path.stat().st_size == 0 for path in media_paths):
        raise ChineseLipsPreparationError("reusable extraction is missing selected media")
    if sum(path.stat().st_size for path in media_paths) != uncompressed_bytes:
        raise ChineseLipsPreparationError("reusable extraction size does not match provenance")
    return ArchiveSelection(
        members=(),
        compressed_bytes=compressed_bytes,
        uncompressed_bytes=uncompressed_bytes,
    )


def prepare_chinese_lips_mini(
    *,
    metadata_path: Path,
    artifact_root: Path,
    repo_id: str,
    revision: str,
    archive_filename: str,
    topic: str,
    clip_count: int,
    speaker: str | None,
    max_compressed_bytes: int,
    reuse_extracted: bool = False,
) -> dict[str, object]:
    """Select, range-read, extract, and compose the bounded R1 dataset slice."""

    if not revision.strip() or revision == "main":
        raise ChineseLipsPreparationError("an immutable dataset revision is required")
    clips = select_clips(metadata_path, topic=topic, count=clip_count, speaker=speaker)
    wanted = processed_member_names(clips)
    extracted_dir = artifact_root / "source" / "extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)
    if reuse_extracted:
        selection = _reuse_extracted_selection(
            artifact_root=artifact_root,
            clips=clips,
            repo_id=repo_id,
            revision=revision,
            archive_filename=archive_filename,
            topic=topic,
            max_compressed_bytes=max_compressed_bytes,
        )
    else:
        filesystem = HfFileSystem()
        remote_path = f"datasets/{repo_id}@{revision}/{archive_filename}"
        with filesystem.open(remote_path, "rb", block_size=256 * 1024) as remote_handle:
            with zipfile.ZipFile(remote_handle) as archive:
                selection = inspect_archive_members(
                    archive,
                    wanted,
                    max_compressed_bytes=max_compressed_bytes,
                )
                for info in selection.members:
                    destination = extracted_dir / PurePosixPath(info.filename).name
                    _copy_member(archive, info, destination)

    selected_payload = {
        "schema_version": 1,
        "dataset_repo": repo_id,
        "dataset_revision": revision,
        "split": "validation",
        "topic": topic,
        "speaker": clips[0].speaker,
        "selection_rule": "speaker_max_clip_count_then_lexicographic; numeric_suffix_ascending",
        "clip_count": len(clips),
        "archive": archive_filename,
        "compressed_bytes": selection.compressed_bytes,
        "uncompressed_bytes": selection.uncompressed_bytes,
        "clips": [clip.to_dict() for clip in clips],
    }
    _write_json(artifact_root / "source" / "selected-clips.json", selected_payload)

    legacy_combined_dir = artifact_root / "source" / "combined"
    if legacy_combined_dir.exists():
        shutil.rmtree(legacy_combined_dir)
    (artifact_root / "concat-list.txt").unlink(missing_ok=True)

    composite_path = artifact_root / "composite.mp4"
    composite_duration_ms, clip_durations_ms = _compose_clips(
        clips,
        extracted_dir,
        composite_path,
    )
    ground_truth: list[dict[str, object]] = []
    cursor_ms = 0
    for clip, duration_ms in zip(clips, clip_durations_ms, strict=True):
        video_path = extracted_dir / f"{clip.clip_id}.mp4"
        audio_path = extracted_dir / f"{clip.clip_id}.wav"
        ground_truth.append(
            {
                "clip_id": clip.clip_id,
                "ordinal": len(ground_truth),
                "start_ms": cursor_ms,
                "end_ms": cursor_ms + duration_ms,
                "gt_text": clip.gt_text,
                "source_video_sha256": _sha256(video_path),
                "source_audio_sha256": _sha256(audio_path),
            }
        )
        cursor_ms += duration_ms

    duration_delta_ms = abs(composite_duration_ms - cursor_ms)
    if duration_delta_ms > max(1000, clip_count * 50):
        raise ChineseLipsPreparationError(
            f"composite duration differs from clip sum by {duration_delta_ms} ms"
        )
    _write_jsonl(artifact_root / "ground-truth.jsonl", ground_truth)

    manifest: dict[str, object] = {
        "schema_version": 1,
        "pipeline_status": "PREPARED",
        "video_id": artifact_root.name,
        "dataset": {
            "repo": repo_id,
            "revision": revision,
            "license": "CC BY-NC-SA 4.0 plus dataset access terms",
            "split": "validation",
            "topic": topic,
            "speaker": clips[0].speaker,
            "clip_count": len(clips),
            "archive": archive_filename,
            "selected_compressed_bytes": selection.compressed_bytes,
            "selected_uncompressed_bytes": selection.uncompressed_bytes,
        },
        "composite": {
            "path": composite_path.name,
            "sha256": _sha256(composite_path),
            "duration_ms": composite_duration_ms,
            "clip_duration_sum_ms": cursor_ms,
            "duration_delta_ms": duration_delta_ms,
        },
        "ground_truth_path": "ground-truth.jsonl",
    }
    _write_json(artifact_root / "dataset-manifest.json", manifest)
    return manifest

import csv
import zipfile
from pathlib import Path

import pytest

from video_evidence_agent.chinese_lips import (
    ChineseLipsPreparationError,
    inspect_archive_members,
    processed_member_names,
    select_clips,
)


def _write_metadata(path: Path) -> None:
    rows = [
        {
            "ID": clip_id,
            "TOPIC": topic,
            "WAV": f"{clip_id}.wav",
            "PPT": f"{clip_id}_PPT.mp4",
            "FACE": f"{clip_id}_FACE.mp4",
            "TEXT": text,
        }
        for clip_id, topic, text in [
            ("speaker-b_KJ_003", "KJ", "第三条内容"),
            ("speaker-a_KJ_002", "KJ", "不应按内容挑选"),
            ("speaker-a_KJ_001", "KJ", "第一条内容"),
            ("speaker-a_KJ_003", "KJ", "第三条内容"),
            ("speaker-b_KJ_001", "KJ", "第一条内容"),
            ("speaker-b_KJ_002", "KJ", "第二条内容"),
            ("speaker-c_ZX_001", "ZX", "其他主题"),
        ]
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ID", "TOPIC", "WAV", "PPT", "FACE", "TEXT"])
        writer.writeheader()
        writer.writerows(rows)


def test_selection_is_deterministic_and_does_not_rank_by_transcript(tmp_path: Path) -> None:
    metadata = tmp_path / "meta.csv"
    _write_metadata(metadata)

    selected = select_clips(metadata, topic="KJ", count=3)

    assert [clip.clip_id for clip in selected] == [
        "speaker-a_KJ_001",
        "speaker-a_KJ_002",
        "speaker-a_KJ_003",
    ]
    assert processed_member_names(selected) == {
        f"processed_val/{clip.clip_id}{suffix}"
        for clip in selected
        for suffix in (".wav", ".mp4")
    }


def test_archive_selection_requires_all_members_and_enforces_budget(tmp_path: Path) -> None:
    archive_path = tmp_path / "processed.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("processed_val/clip-001.wav", b"audio")
        archive.writestr("processed_val/clip-001.mp4", b"video")

    wanted = {"processed_val/clip-001.wav", "processed_val/clip-001.mp4"}
    with zipfile.ZipFile(archive_path) as archive:
        selected = inspect_archive_members(archive, wanted, max_compressed_bytes=100)
        assert len(selected.members) == 2

    with zipfile.ZipFile(archive_path) as archive:
        with pytest.raises(ChineseLipsPreparationError, match="budget"):
            inspect_archive_members(archive, wanted, max_compressed_bytes=1)

    with zipfile.ZipFile(archive_path) as archive:
        with pytest.raises(ChineseLipsPreparationError, match="missing"):
            inspect_archive_members(
                archive,
                wanted | {"processed_val/clip-002.wav"},
                max_compressed_bytes=100,
            )

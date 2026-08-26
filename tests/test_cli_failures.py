import argparse
import json
from pathlib import Path

import pytest

from video_evidence_agent import cli
from video_evidence_agent.asr import AsrError
from video_evidence_agent.audio import AudioExtraction, AudioProbe


def test_asr_failure_invalidates_a_prior_success_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"placeholder")
    artifacts = tmp_path / "artifacts"
    manifest_path = artifacts / "smoke-001" / "manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(
        json.dumps({"pipeline_status": "SUCCEEDED", "video_id": "smoke-001"}),
        encoding="utf-8",
    )

    def fake_extract(media_path: Path, output_path: Path, **kwargs: object) -> AudioExtraction:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"audio")
        return AudioExtraction(
            path=output_path,
            command=("ffmpeg",),
            probe=AudioProbe(
                path=output_path,
                channels=1,
                sample_rate_hz=16_000,
                duration_ms=600_000,
            ),
        )

    monkeypatch.setattr(cli, "probe_media_duration_ms", lambda path: 600_000)
    monkeypatch.setattr(cli, "extract_audio", fake_extract)
    monkeypatch.setattr(
        cli,
        "transcribe_audio",
        lambda *args, **kwargs: (_ for _ in ()).throw(AsrError("ASR failed")),
    )

    args = argparse.Namespace(
        video_id="smoke-001",
        video_path=str(source),
        artifacts_dir=artifacts,
        preview_seconds=300,
        asr_model="test-model",
        target_segment_ms=45_000,
        max_segment_ms=60_000,
        source_url="https://example.test/source",
        source_license="CC BY-SA 4.0",
        source_attribution="Example creator",
        source_use_note="local smoke only",
    )

    with pytest.raises(AsrError, match="ASR failed"):
        cli._ingest(args)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["pipeline_status"] == "FAILED"
    assert manifest["failure"]["stage"] == "asr_preview"
    assert manifest["source"]["origin_url"] == "https://example.test/source"

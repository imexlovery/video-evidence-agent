"""Bounded public Bilibili URL download and existing-ingest composition."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qsl, urlsplit

from dotenv import load_dotenv

from .planning import PlanningError

BILIBILI_HOSTS = frozenset({"bilibili.com", "www.bilibili.com"})
URL_INGEST_SCHEMA_VERSION = "visual-report-url-ingest.v1a-local-mvp"
_BVID_PATTERN = re.compile(r"BV[0-9A-Za-z]{10}")
_PAGE_PATTERN = re.compile(r"[0-9]+")
_SOURCE_NAME = "source"
_MAX_VIDEO_TITLE_LENGTH = 160
_MAX_ATTRIBUTION_LENGTH = 300

CommandRunner = Callable[..., Any]


@dataclass(frozen=True)
class BilibiliSource:
    """The validated public source URL and its stable BVID identity."""

    bvid: str
    submitted_url: str
    canonical_url: str

    @property
    def video_id(self) -> str:
        return f"bilibili-{self.bvid}"


@dataclass(frozen=True)
class DownloadResult:
    """Verified yt-dlp output and public metadata."""

    source: BilibiliSource
    media_path: Path
    info_path: Path
    title: str
    uploader: str
    attribution: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class IngestResult:
    """The existing ingest command's run-local output boundary."""

    video_id: str
    artifact_root: Path
    manifest_path: Path
    segments_path: Path
    command: tuple[str, ...]


class UrlIngestError(PlanningError):
    """A safe, stable failure from the URL/download/ingest boundary."""


def _parse_bilibili_url(value: object) -> tuple[str, str, str]:
    if not isinstance(value, str):
        raise UrlIngestError("URL_INVALID", "url must be a string")
    submitted_url = value.strip()
    try:
        parsed = urlsplit(submitted_url)
        hostname = parsed.hostname.lower() if parsed.hostname else None
        port = parsed.port
    except ValueError as exc:
        raise UrlIngestError("URL_INVALID", "url is not a valid HTTPS Bilibili URL") from exc
    if parsed.scheme != "https" or hostname not in BILIBILI_HOSTS:
        raise UrlIngestError("URL_INVALID", "url must use HTTPS and a Bilibili host")
    if parsed.username or parsed.password or port is not None:
        raise UrlIngestError("URL_INVALID", "url must not include credentials or a port")
    if parsed.fragment:
        raise UrlIngestError("URL_INVALID", "url must not include a fragment")
    match = re.fullmatch(r"/video/(BV[0-9A-Za-z]{10})/?", parsed.path)
    if match is None or _BVID_PATTERN.fullmatch(match.group(1)) is None:
        raise UrlIngestError("URL_INVALID", "url must use /video/<BVID>")
    bvid = match.group(1)
    page = next(
        (
            value
            for key, value in parse_qsl(parsed.query, keep_blank_values=True)
            if key == "p" and _PAGE_PATTERN.fullmatch(value) is not None
        ),
        None,
    )
    canonical_url = f"https://www.bilibili.com/video/{bvid}/"
    if page is not None:
        canonical_url += f"?p={page}"
    return submitted_url, bvid, canonical_url


def clean_bilibili_url(value: object) -> str:
    """Keep the BVID and an optional numeric page, dropping other URL data."""

    return _parse_bilibili_url(value)[2]


def validate_bilibili_url(value: object) -> BilibiliSource:
    """Validate and clean one public Bilibili BV URL without side effects."""

    submitted_url, bvid, canonical_url = _parse_bilibili_url(value)
    return BilibiliSource(
        bvid=bvid,
        submitted_url=submitted_url,
        canonical_url=canonical_url,
    )


def _run_command(
    command: list[str], runner: CommandRunner | None, *, category: str
) -> Any:
    active_runner = runner or subprocess.run
    try:
        return active_runner(
            command,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise UrlIngestError(category, "external command could not be started") from exc


def _inside(path: Path, root: Path, *, category: str, message: str) -> Path:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise UrlIngestError(category, message) from exc
    return resolved_path


def _printed_media_path(stdout: object, download_dir: Path) -> Path:
    if not isinstance(stdout, str):
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp did not report a media path")
    for line in reversed(stdout.splitlines()):
        candidate_text = line.strip()
        if not candidate_text:
            continue
        candidate = Path(candidate_text)
        if not candidate.is_absolute():
            candidate = download_dir / candidate
        if candidate.name.startswith(f"{_SOURCE_NAME}.") and candidate.name != "source.info.json":
            return candidate
    raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp did not report a media path")


def _metadata(info_path: Path, source: BilibiliSource) -> tuple[str, str, str]:
    try:
        payload = json.loads(info_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp metadata is unavailable") from exc
    if not isinstance(payload, dict):
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp metadata is invalid")
    title = payload.get("title")
    uploader = payload.get("uploader") or payload.get("channel")
    if not isinstance(title, str) or not title.strip():
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp metadata has no title")
    if not isinstance(uploader, str) or not uploader.strip():
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp metadata has no uploader")
    title = title.strip()
    uploader = uploader.strip()
    attribution = f"Bilibili；{uploader}；《{title}》；{source.canonical_url}"
    if len(title) > _MAX_VIDEO_TITLE_LENGTH or len(attribution) > _MAX_ATTRIBUTION_LENGTH:
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp metadata exceeds report limits")
    return title, uploader, attribution


def download_bilibili_video(
    source: BilibiliSource,
    run_dir: Path,
    *,
    runner: CommandRunner | None = None,
) -> DownloadResult:
    """Run the frozen yt-dlp command and verify its run-local output."""

    executable = shutil.which("yt-dlp")
    if executable is None:
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp is unavailable")
    download_dir = run_dir.resolve() / "download"
    try:
        download_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise UrlIngestError("DOWNLOAD_ERROR", "download directory is unavailable") from exc
    command = [
        executable,
        "--ignore-config",
        "--no-playlist",
        "-P",
        str(download_dir),
        "-o",
        "source.%(ext)s",
        "-S",
        "res:1080,vcodec:h264,acodec:aac",
        "--merge-output-format",
        "mp4",
        "--write-info-json",
        "--print",
        "after_move:filepath",
        source.canonical_url,
    ]
    completed = _run_command(command, runner, category="DOWNLOAD_ERROR")
    if getattr(completed, "returncode", 1) != 0:
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp failed")
    media_path = _inside(
        _printed_media_path(getattr(completed, "stdout", None), download_dir),
        download_dir,
        category="DOWNLOAD_ERROR",
        message="downloaded media path is outside the run directory",
    )
    if not media_path.is_file() or media_path.stat().st_size == 0:
        raise UrlIngestError("DOWNLOAD_ERROR", "downloaded media is missing")
    info_path = download_dir / "source.info.json"
    if not info_path.is_file():
        raise UrlIngestError("DOWNLOAD_ERROR", "yt-dlp metadata file is missing")
    title, uploader, attribution = _metadata(info_path, source)
    return DownloadResult(
        source=source,
        media_path=media_path,
        info_path=info_path.resolve(),
        title=title,
        uploader=uploader,
        attribution=attribution,
        command=tuple(command),
    )


def ingest_downloaded_video(
    download: DownloadResult,
    run_dir: Path,
    *,
    runner: CommandRunner | None = None,
) -> IngestResult:
    """Invoke the existing ``video-evidence ingest`` command once."""

    executable = shutil.which("video-evidence")
    if executable is None:
        raise UrlIngestError("INGEST_ERROR", "video-evidence command is unavailable")
    run_dir = run_dir.resolve()
    ingest_root = run_dir / "ingest"
    try:
        ingest_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise UrlIngestError("INGEST_ERROR", "ingest directory is unavailable") from exc
    video_id = download.source.video_id
    command = [
        executable,
        "ingest",
        str(download.media_path),
        "--video-id",
        video_id,
        "--artifacts-dir",
        str(ingest_root),
        "--source-url",
        download.source.canonical_url,
        "--source-attribution",
        download.attribution,
        "--source-use-note",
        "Task 011 local MVP; public Bilibili source; raw media remains local",
    ]
    load_dotenv(Path(__file__).resolve().parents[3] / ".env", override=False)
    completed = _run_command(command, runner, category="INGEST_ERROR")
    artifact_root = ingest_root / video_id
    manifest_path = artifact_root / "manifest.json"
    segments_path = artifact_root / "segments.jsonl"
    if getattr(completed, "returncode", 1) != 0:
        raise UrlIngestError("INGEST_ERROR", "video-evidence ingest failed")
    if not manifest_path.is_file() or not segments_path.is_file():
        raise UrlIngestError("INGEST_ERROR", "ingest did not produce manifest and segments")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UrlIngestError("INGEST_ERROR", "ingest manifest is unavailable") from exc
    if (
        not isinstance(manifest, dict)
        or manifest.get("pipeline_status") != "SUCCEEDED"
        or manifest.get("video_id") != video_id
    ):
        raise UrlIngestError("INGEST_ERROR", "ingest manifest is not successful")
    return IngestResult(
        video_id=video_id,
        artifact_root=artifact_root.resolve(),
        manifest_path=manifest_path.resolve(),
        segments_path=segments_path.resolve(),
        command=tuple(command),
    )


__all__ = [
    "BILIBILI_HOSTS",
    "BilibiliSource",
    "DownloadResult",
    "IngestResult",
    "URL_INGEST_SCHEMA_VERSION",
    "UrlIngestError",
    "clean_bilibili_url",
    "download_bilibili_video",
    "ingest_downloaded_video",
    "validate_bilibili_url",
]

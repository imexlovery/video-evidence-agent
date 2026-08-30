"""Pydantic contracts for the renderer-first visual report prototype."""

from __future__ import annotations

from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, model_validator

PLAN_SCHEMA_VERSION = "visual-report.v0-prototype"
ASSET_SCHEMA_VERSION = "visual-report-assets.v0-prototype"


class StrictModel(BaseModel):
    """Small frozen contract base that rejects unknown fields and blank strings."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    @model_validator(mode="after")
    def strings_must_not_be_blank(self) -> "StrictModel":
        for field_name, value in self.__dict__.items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{field_name} must not be blank")
        return self


class SourceRef(StrictModel):
    segment_id: str = Field(min_length=1, max_length=100)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)

    @model_validator(mode="after")
    def end_must_follow_start(self) -> "SourceRef":
        if self.end_ms <= self.start_ms:
            raise ValueError("source ref end_ms must be greater than start_ms")
        return self


class VideoMeta(StrictModel):
    video_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=160)
    duration_ms: int = Field(gt=0)
    source_url: str = Field(min_length=1, max_length=300)
    attribution: str = Field(min_length=1, max_length=300)


class HeroContent(StrictModel):
    eyebrow: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=120)
    tldr: str = Field(min_length=1, max_length=320)


class BlockBase(StrictModel):
    block_id: str = Field(min_length=1, max_length=80)
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, max_length=4)
    asset_id: str | None = Field(default=None, min_length=1, max_length=80)


class InsightCardBlock(BlockBase):
    type: Literal["insight_card"]
    headline: str = Field(min_length=1, max_length=140)
    body: str = Field(min_length=1, max_length=420)


class BulletGroupBlock(BlockBase):
    type: Literal["bullet_group"]
    headline: str = Field(min_length=1, max_length=140)
    items: tuple[str, ...] = Field(min_length=2, max_length=5)


class MetricItem(StrictModel):
    value: str = Field(min_length=1, max_length=30)
    label: str = Field(min_length=1, max_length=80)
    context: str | None = Field(default=None, min_length=1, max_length=140)


class MetricRowBlock(BlockBase):
    type: Literal["metric_row"]
    headline: str = Field(min_length=1, max_length=140)
    items: tuple[MetricItem, ...] = Field(min_length=2, max_length=4)


class ComparisonSide(StrictModel):
    label: str = Field(min_length=1, max_length=40)
    items: tuple[str, ...] = Field(min_length=1, max_length=4)


class ComparisonCardBlock(BlockBase):
    type: Literal["comparison_card"]
    headline: str = Field(min_length=1, max_length=140)
    left: ComparisonSide
    right: ComparisonSide


class ProcessStep(StrictModel):
    title: str = Field(min_length=1, max_length=80)
    body: str = Field(min_length=1, max_length=180)


class ProcessFlowBlock(BlockBase):
    type: Literal["process_flow"]
    headline: str = Field(min_length=1, max_length=140)
    steps: tuple[ProcessStep, ...] = Field(min_length=3, max_length=6)


class ImageCaptionBlock(BlockBase):
    type: Literal["image_caption"]
    headline: str = Field(min_length=1, max_length=140)
    body: str | None = Field(default=None, min_length=1, max_length=260)
    asset_id: str = Field(min_length=1, max_length=80)


class TakeawayBoxBlock(BlockBase):
    type: Literal["takeaway_box"]
    headline: str = Field(min_length=1, max_length=140)
    takeaways: tuple[str, ...] = Field(min_length=2, max_length=5)


Block: TypeAlias = Annotated[
    InsightCardBlock
    | BulletGroupBlock
    | MetricRowBlock
    | ComparisonCardBlock
    | ProcessFlowBlock
    | ImageCaptionBlock
    | TakeawayBoxBlock,
    Field(discriminator="type"),
]


class Section(StrictModel):
    section_id: str = Field(min_length=1, max_length=80)
    kicker: str = Field(min_length=1, max_length=80)
    title: str = Field(min_length=1, max_length=160)
    timestamp_ms: int = Field(ge=0)
    blocks: tuple[Block, ...] = Field(min_length=1, max_length=7)


class ReportPlan(StrictModel):
    schema_version: Literal[PLAN_SCHEMA_VERSION]
    report_id: str = Field(min_length=1, max_length=80)
    video: VideoMeta
    hero: HeroContent
    sections: tuple[Section, ...] = Field(min_length=3, max_length=5)

    @model_validator(mode="after")
    def validate_ids_and_source_boundaries(self) -> "ReportPlan":
        section_ids = [section.section_id for section in self.sections]
        if len(section_ids) != len(set(section_ids)):
            raise ValueError("section IDs must be unique")

        block_ids: list[str] = []
        expected_segment_prefix = f"{self.video.video_id}-seg-"
        for section in self.sections:
            if section.timestamp_ms > self.video.duration_ms:
                raise ValueError(
                    f"section {section.section_id} timestamp_ms exceeds video duration"
                )
            for block in section.blocks:
                block_ids.append(block.block_id)
                for source_ref in block.source_refs:
                    if not source_ref.segment_id.startswith(expected_segment_prefix):
                        raise ValueError(
                            f"source ref {source_ref.segment_id} does not belong to video "
                            f"{self.video.video_id}"
                        )
                    if source_ref.end_ms > self.video.duration_ms:
                        raise ValueError(
                            f"source ref {source_ref.segment_id} exceeds video duration"
                        )
        if len(block_ids) != len(set(block_ids)):
            raise ValueError("block IDs must be unique")
        return self


class AssetRecord(StrictModel):
    asset_id: str = Field(min_length=1, max_length=80)
    type: Literal["keyframe"]
    timestamp_ms: int = Field(ge=0)
    path: str = Field(min_length=1, max_length=300)
    alt: str = Field(min_length=1, max_length=220)
    caption: str = Field(min_length=1, max_length=260)


class AssetManifest(StrictModel):
    schema_version: Literal[ASSET_SCHEMA_VERSION]
    assets: tuple[AssetRecord, ...] = Field(max_length=8)

    @model_validator(mode="after")
    def asset_ids_must_be_unique(self) -> "AssetManifest":
        asset_ids = [asset.asset_id for asset in self.assets]
        if len(asset_ids) != len(set(asset_ids)):
            raise ValueError("asset IDs must be unique")
        return self

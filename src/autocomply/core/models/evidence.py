"""Evidence domain model.

Evidence represents raw data collected from the system that proves (or disproves)
whether a control is being met. It is always tied to a specific collector
and a specific point in time.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EvidenceSource(str, Enum):
    """The source system from which evidence was collected."""

    WINDOWS_REGISTRY = "windows_registry"
    WINDOWS_SERVICES = "windows_services"
    WINDOWS_EVENT_LOG = "windows_event_log"
    WINDOWS_FIREWALL = "windows_firewall"
    WINDOWS_USERS = "windows_users"
    NETWORK = "network"
    FILE_SYSTEM = "file_system"
    CLOUD = "cloud"
    MANUAL = "manual"


class Evidence(BaseModel):
    """Raw data collected from the system for a specific control.

    Evidence is immutable once collected — it represents a snapshot
    of the system state at a specific point in time.

    Attributes:
        control_id: The control this evidence relates to.
        source: Where the evidence was collected from.
        title: Short description of what was checked.
        raw_data: The actual data collected from the system.
        collected_at: When the evidence was collected (UTC).
        collector_version: Version of the collector that gathered this evidence.
        metadata: Optional additional context about the collection.
    """

    control_id: str = Field(
        ...,
        description="The control this evidence relates to.",
        examples=["CIS-1.1"],
    )
    source: EvidenceSource = Field(
        ...,
        description="Where the evidence was collected from.",
    )
    title: str = Field(
        ...,
        description="Short description of what was checked.",
        examples=["Windows Firewall Domain Profile Status"],
    )
    raw_data: dict[str, Any] = Field(
        ...,
        description="The actual data collected from the system.",
    )
    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the evidence was collected (UTC).",
    )
    collector_version: str = Field(
        default="1.0.0",
        description="Version of the collector that gathered this evidence.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional additional context about the collection.",
    )

    @field_validator("collected_at")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        """Ensure all timestamps are timezone-aware UTC."""
        if v.tzinfo is None:
            return v.replace(tzinfo=UTC)
        return v

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
    }

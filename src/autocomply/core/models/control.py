"""Control domain model.

A Control represents a single security safeguard from a compliance framework
(e.g., CIS Controls v8, NIST CSF). It defines *what* should be checked,
not *how* to check it — that is the responsibility of the collectors.
"""

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity level of a control.

    Inherits from str so that JSON serialization works automatically.
    """

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ControlGroup(str, Enum):
    """Top-level grouping of controls within a framework.

    For CIS Controls v8, these map to Implementation Groups (IG1/IG2/IG3).
    """

    IG1 = "ig1"  # Basic cyber hygiene — all organizations
    IG2 = "ig2"  # Intermediate — organizations with IT staff
    IG3 = "ig3"  # Advanced — mature security programs


class Control(BaseModel):
    """A single security control from a compliance framework.

    Attributes:
        control_id: Unique identifier within the framework (e.g., "CIS-1.1").
        title: Short human-readable name of the control.
        description: Full description of what the control requires.
        severity: How critical this control is to overall security posture.
        group: Implementation group this control belongs to.
        framework: The framework this control comes from (e.g., "cis_v8").
        automated: Whether this control can be checked automatically.
        references: Optional list of external references or documentation URLs.
    """

    control_id: str = Field(
        ...,
        description="Unique identifier within the framework.",
        examples=["CIS-1.1", "CIS-2.3"],
    )
    title: str = Field(
        ...,
        description="Short human-readable name of the control.",
        examples=["Establish and Maintain a Software Inventory"],
    )
    description: str = Field(
        ...,
        description="Full description of what the control requires.",
    )
    severity: Severity = Field(
        ...,
        description="How critical this control is.",
    )
    group: ControlGroup = Field(
        ...,
        description="Implementation group this control belongs to.",
    )
    framework: str = Field(
        ...,
        description="The framework this control comes from.",
        examples=["cis_v8", "nist_csf", "iso27001"],
    )
    automated: bool = Field(
        default=True,
        description="Whether this control can be assessed automatically.",
    )
    references: list[str] = Field(
        default_factory=list,
        description="External references or documentation URLs.",
    )

    model_config = {
        "frozen": True,  # Controls are immutable — they come from framework definitions
        "str_strip_whitespace": True,
    }

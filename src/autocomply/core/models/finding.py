"""Finding domain model.

A Finding is the result of evaluating a Control against collected Evidence.
It represents the compliance status of a single control at a specific point
in time — the core output of AutoComply's assessment engine.
"""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator

from autocomply.core.models.control import Control, Severity
from autocomply.core.models.evidence import Evidence


class FindingStatus(str, Enum):
    """The compliance status of a control after evaluation.

    PASS: Evidence confirms the control is being met.
    FAIL: Evidence confirms the control is NOT being met.
    ERROR: The collector encountered an error during evidence collection.
    MANUAL_REVIEW: The control cannot be assessed automatically.
    NOT_APPLICABLE: The control does not apply to this environment.
    """

    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    MANUAL_REVIEW = "manual_review"
    NOT_APPLICABLE = "not_applicable"


class Finding(BaseModel):
    """The result of evaluating a single control against collected evidence.

    A Finding ties together a Control, its Evidence, and the resulting
    compliance status. It is the primary output of the compliance engine
    and the primary input to the reporting module.

    Attributes:
        control: The control that was evaluated.
        status: Whether the control passed, failed, or could not be assessed.
        evidence: The evidence collected during assessment.
        message: Human-readable explanation of the finding.
        remediation: Suggested steps to fix a failing control.
        assessed_at: When the assessment was performed (UTC).
        risk_score: Numeric risk score (0-100). Higher = more risk.
    """

    control: Control = Field(
        ...,
        description="The control that was evaluated.",
    )
    status: FindingStatus = Field(
        ...,
        description="The compliance status of this control.",
    )
    evidence: list[Evidence] = Field(
        default_factory=list,
        description="Evidence collected during assessment.",
    )
    message: str = Field(
        ...,
        description="Human-readable explanation of the finding.",
        examples=["Windows Firewall is enabled on all profiles."],
    )
    remediation: str | None = Field(
        default=None,
        description="Suggested steps to remediate a failing control.",
    )
    assessed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the assessment was performed (UTC).",
    )
    risk_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Numeric risk score (0-100). Higher means more risk.",
    )

    @model_validator(mode="after")
    def set_risk_score(self) -> "Finding":
        """Automatically calculate risk score based on status and severity.

        Risk score logic:
        - PASS or NOT_APPLICABLE: always 0
        - FAIL: score depends on control severity
        - ERROR or MANUAL_REVIEW: medium risk by default
        """
        if self.status in (FindingStatus.PASS, FindingStatus.NOT_APPLICABLE):
            object.__setattr__(self, "risk_score", 0)
            return self

        if self.status == FindingStatus.FAIL:
            severity_scores = {
                Severity.CRITICAL: 100,
                Severity.HIGH: 75,
                Severity.MEDIUM: 50,
                Severity.LOW: 25,
                Severity.INFO: 10,
            }
            score = severity_scores.get(self.control.severity, 50)
            object.__setattr__(self, "risk_score", score)
            return self

        # ERROR or MANUAL_REVIEW
        object.__setattr__(self, "risk_score", 40)
        return self

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
    }

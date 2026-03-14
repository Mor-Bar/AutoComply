"""Unit tests for core domain models."""

from datetime import UTC

import pytest
from autocomply.core.models.control import Control, ControlGroup, Severity
from autocomply.core.models.evidence import Evidence, EvidenceSource
from autocomply.core.models.finding import Finding, FindingStatus

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_control() -> Control:
    """A minimal valid Control for use in tests."""
    return Control(
        control_id="CIS-4.1",
        title="Establish and Maintain a Secure Configuration Process",
        description="Establish and maintain a secure configuration process for enterprise assets.",
        severity=Severity.HIGH,
        group=ControlGroup.IG1,
        framework="cis_v8",
    )


@pytest.fixture()
def sample_evidence(sample_control: Control) -> Evidence:
    """A minimal valid Evidence for use in tests."""
    return Evidence(
        control_id=sample_control.control_id,
        source=EvidenceSource.WINDOWS_REGISTRY,
        title="Windows Firewall Domain Profile",
        raw_data={"firewall_enabled": True, "profile": "domain"},
    )


# ---------------------------------------------------------------------------
# Control tests
# ---------------------------------------------------------------------------


class TestControl:
    def test_create_valid_control(self, sample_control: Control) -> None:
        assert sample_control.control_id == "CIS-4.1"
        assert sample_control.severity == Severity.HIGH
        assert sample_control.automated is True
        assert sample_control.references == []

    def test_control_is_immutable(self, sample_control: Control) -> None:
        with pytest.raises(Exception):
            object.__setattr__(sample_control, "control_id", "CIS-9.9")

    def test_severity_serializes_as_string(self) -> None:
        assert Severity.HIGH.value == "high"
        assert Severity.CRITICAL.value == "critical"

    def test_control_group_serializes_as_string(self) -> None:
        assert ControlGroup.IG1.value == "ig1"


# ---------------------------------------------------------------------------
# Evidence tests
# ---------------------------------------------------------------------------


class TestEvidence:
    def test_create_valid_evidence(self, sample_evidence: Evidence) -> None:
        assert sample_evidence.control_id == "CIS-4.1"
        assert sample_evidence.source == EvidenceSource.WINDOWS_REGISTRY
        assert sample_evidence.raw_data["firewall_enabled"] is True

    def test_collected_at_is_utc(self, sample_evidence: Evidence) -> None:
        assert sample_evidence.collected_at.tzinfo == UTC

    def test_evidence_is_immutable(self, sample_evidence: Evidence) -> None:
        with pytest.raises(Exception):
            object.__setattr__(sample_evidence, "title", "changed")


# ---------------------------------------------------------------------------
# Finding tests
# ---------------------------------------------------------------------------


class TestFinding:
    def test_passing_finding_has_zero_risk(
        self, sample_control: Control, sample_evidence: Evidence
    ) -> None:
        finding = Finding(
            control=sample_control,
            status=FindingStatus.PASS,
            evidence=[sample_evidence],
            message="Firewall is enabled.",
        )
        assert finding.risk_score == 0

    def test_failing_high_severity_has_correct_risk(
        self, sample_control: Control
    ) -> None:
        finding = Finding(
            control=sample_control,
            status=FindingStatus.FAIL,
            message="Firewall is disabled.",
            remediation="Enable Windows Firewall on all profiles.",
        )
        assert finding.risk_score == 75

    def test_failing_critical_severity_has_max_risk(self) -> None:
        critical_control = Control(
            control_id="CIS-1.1",
            title="Critical Control",
            description="A critical control.",
            severity=Severity.CRITICAL,
            group=ControlGroup.IG1,
            framework="cis_v8",
        )
        finding = Finding(
            control=critical_control,
            status=FindingStatus.FAIL,
            message="Control failed.",
        )
        assert finding.risk_score == 100

    def test_not_applicable_has_zero_risk(self, sample_control: Control) -> None:
        finding = Finding(
            control=sample_control,
            status=FindingStatus.NOT_APPLICABLE,
            message="Not applicable in this environment.",
        )
        assert finding.risk_score == 0

    def test_error_status_has_medium_risk(self, sample_control: Control) -> None:
        finding = Finding(
            control=sample_control,
            status=FindingStatus.ERROR,
            message="Collector encountered an error.",
        )
        assert finding.risk_score == 40

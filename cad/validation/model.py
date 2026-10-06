"""Data contracts for validation reports.

The contracts are intentionally independent of build123d, CadQuery, and mesh
libraries so that the rule logic can be tested before detailed CAD exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from cad.parameters import RangeMm

Vector3Mm = tuple[float, float, float]


class ValidationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    NOT_READY = "not-ready"
    NOT_APPLICABLE = "not-applicable"


class IssueSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ValidationIssue:
    """One rule result with enough context for a reviewable report."""

    rule_id: str
    status: ValidationStatus
    severity: IssueSeverity
    message: str
    component: str | None = None
    evidence: str | None = None

    @property
    def blocks_release(self) -> bool:
        return self.severity == IssueSeverity.ERROR and self.status in {
            ValidationStatus.FAIL,
            ValidationStatus.NOT_READY,
        }


@dataclass
class ValidationReport:
    """Collection of issues produced by one validation run."""

    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    def extend(self, other: "ValidationReport") -> None:
        self.issues.extend(other.issues)

    @property
    def blocking_issues(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.blocks_release]

    @property
    def passed(self) -> bool:
        return not self.blocking_issues

    @property
    def status(self) -> ValidationStatus:
        if any(issue.status == ValidationStatus.FAIL for issue in self.issues):
            return ValidationStatus.FAIL
        if any(issue.status == ValidationStatus.NOT_READY for issue in self.issues):
            return ValidationStatus.NOT_READY
        return ValidationStatus.PASS


@dataclass(frozen=True)
class WorkingEnvelopeRequirement:
    """Tool-point travel target, separate from rail or screw length."""

    x_travel_mm: float
    y_travel_mm: float
    z_travel_mm: RangeMm


@dataclass(frozen=True)
class AxisCapacity:
    """Usable axis travel after all mechanical end margins."""

    x_travel_mm: float
    y_travel_mm: float
    z_travel_mm: float


@dataclass(frozen=True)
class PrintOrientationCandidate:
    """A documented candidate orientation for a printable component."""

    name: str
    extents_mm: Vector3Mm
    manufacturing_notes: str


@dataclass(frozen=True)
class PrintablePart:
    """Printability evidence supplied by a future part module."""

    name: str
    orientations: tuple[PrintOrientationCandidate, ...]
    minimum_wall_thickness_mm: float | None = None
    minimum_fastener_edge_distance_mm: float | None = None


@dataclass(frozen=True)
class RuleDefinition:
    """Stable catalog entry for a validation rule."""

    rule_id: str
    description: str
    first_required_phase: int
    geometry_required: bool

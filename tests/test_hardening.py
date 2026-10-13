"""Security and numeric validation regressions."""
import math

import pytest
from pydantic import ValidationError

from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor


def payload(**kwargs):
    data = {"task_id": "T", "target_identifier": "KEY", "primary_metric": 25.0}
    data.update(kwargs)
    return SystemTaskPayload(**data)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_metrics_rejected(value):
    with pytest.raises(ValidationError):
        payload(primary_metric=value)
    with pytest.raises(ValidationError):
        payload(secondary_metric=value)


def test_metadata_phi_does_not_enter_audit():
    supervisor = SystemSupervisor()
    with pytest.raises(SecurityException):
        supervisor.process_task(payload(attributes={"nested": {"contact": "user@example.com"}}))
    assert supervisor.dossier_registry == {}


def test_hmac_not_ambiguous_when_fields_contain_separator():
    trail = AuditTrail(secret_key="testing-only")
    trail.log("a|b", "c", "EVENT", {"ok": True})
    assert trail.verify_integrity()
    trail.logs[0]["actor"] = "a"
    trail.logs[0]["actor_tier"] = "b|c"
    assert not trail.verify_integrity()


def test_malformed_audit_entry_reports_invalid():
    trail = AuditTrail(secret_key="testing-only")
    trail.log("actor", "tier", "EVENT", {})
    del trail.logs[0]["timestamp"]
    assert not trail.verify_integrity()


def test_api_rejects_sensitive_metadata():
    from fastapi.testclient import TestClient
    from agents.api import app
    response = TestClient(app).post("/api/audit", json={
        "task_id": "T", "target_identifier": "KEY", "primary_metric": 1,
        "attributes": {"contact": "user@example.com"},
    })
    assert response.status_code == 422
    assert "user@example.com" not in response.text

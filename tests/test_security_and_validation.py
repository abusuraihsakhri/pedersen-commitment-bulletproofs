"""
Automated Pytest for security audit and input validation in Pedersen Commitment Bulletproofs.
Domain: Post-Quantum Cryptography & Hardware Security
"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import warnings
from agents.base import AuditTrail, PHIGuard, SecurityException, assert_no_phi


class TestAuditTrailSecurity:
    """Tests for HMAC-SHA256 audit trail security properties."""

    def test_audit_trail_requires_secret_or_env(self):
        """AuditTrail should warn and use ephemeral key when no secret is provided."""
        # Ensure env var is not set for this test
        original = os.environ.pop("AUDIT_SECRET_KEY", None)
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                trail = AuditTrail()
                # Should have issued a warning about missing secret
                assert any("AUDIT_SECRET_KEY" in str(warning.message) for warning in w)
                # Should still have a key (ephemeral random)
                assert len(trail.secret_key) > 0
        finally:
            if original is not None:
                os.environ["AUDIT_SECRET_KEY"] = original

    def test_audit_trail_uses_provided_key(self):
        """AuditTrail should use the key provided via constructor."""
        trail = AuditTrail(secret_key="test-key-for-unit-tests")
        assert trail.secret_key == b"test-key-for-unit-tests"

    def test_audit_trail_uses_env_key(self):
        """AuditTrail should use the key from environment variable."""
        os.environ["AUDIT_SECRET_KEY"] = "env-based-test-key"
        try:
            trail = AuditTrail()
            assert trail.secret_key == b"env-based-test-key"
        finally:
            os.environ.pop("AUDIT_SECRET_KEY", None)

    def test_audit_trail_logs_and_verifies(self):
        """Audit trail should maintain integrity across multiple log entries."""
        trail = AuditTrail(secret_key="integrity-test-key")
        trail.log("test_actor", "tier1", "TEST_EVENT", {"data": "value1"})
        trail.log("test_actor", "tier1", "TEST_EVENT", {"data": "value2"})
        assert len(trail.get_trail()) == 2
        assert trail.verify_integrity() is True

    def test_audit_trail_tamper_detection(self):
        """Audit trail should detect tampered entries."""
        trail = AuditTrail(secret_key="tamper-test-key")
        trail.log("actor", "tier", "EVENT", {"data": "original"})
        # Tamper with the entry
        trail.logs[0]["payload_hash"] = "tampered_hash"
        assert trail.verify_integrity() is False


class TestPHIGuard:
    """Tests for PHI outbound guard patterns."""

    def test_phi_guard_blocks_mrn(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Patient MRN-12345678")

    def test_phi_guard_blocks_ssn(self):
        with pytest.raises(SecurityException):
            assert_no_phi("SSN: 123-45-6789")

    def test_phi_guard_blocks_phone(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Call (555) 123-4567")

    def test_phi_guard_blocks_email(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Contact user@example.com")

    def test_phi_guard_blocks_dob(self):
        with pytest.raises(SecurityException):
            assert_no_phi("DOB: 01/15/1990")

    def test_phi_guard_blocks_patient_name(self):
        with pytest.raises(SecurityException):
            assert_no_phi("Patient Name John Smith")

    def test_phi_guard_allows_safe_text(self):
        """Clean analytical text should pass without exception."""
        assert_no_phi("Analytical assay specimen KEY-001 optimal") is None

    def test_phi_guard_handles_empty(self):
        """Empty string should not raise."""
        assert_no_phi("") is None

    def test_phi_guard_handles_none(self):
        """None should not raise."""
        assert_no_phi(None) is None

    def test_phi_redaction(self):
        """PHIGuard.redact_phi should replace PHI with placeholder."""
        redacted = PHIGuard.redact_phi("Contact user@example.com or MRN-12345")
        assert "user@example.com" not in redacted
        assert "MRN-12345" not in redacted
        assert "[REDACTED_IDENTIFIER]" in redacted


class TestBatchCLIValidation:
    """Tests for batch CLI input validation."""

    def test_batch_missing_file_returns_error(self, tmp_path):
        """Batch command should return error code for missing input file."""
        from cli import main
        nonexistent = str(tmp_path / "nonexistent.csv")
        result = main(["batch", "-i", nonexistent, "-o", str(tmp_path / "out.csv")])
        assert result == 1

    def test_batch_processes_valid_csv(self, tmp_path):
        """Batch command should process valid CSV without errors."""
        from cli import main
        input_csv = tmp_path / "input.csv"
        input_csv.write_text(
            "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
            "T1,KEY-01,12.0,4.0,False,NOMINAL\n"
            "T2,KEY-02,35.0,15.0,True,DISCORDANT\n",
            encoding="utf-8",
        )
        output_csv = tmp_path / "output.csv"
        result = main(["batch", "-i", str(input_csv), "-o", str(output_csv)])
        assert result == 0
        assert output_csv.exists()
        content = output_csv.read_text(encoding="utf-8")
        assert "overall_urgency" in content

    def test_batch_skips_invalid_rows(self, tmp_path, capsys):
        """Batch command should skip rows with invalid numeric data."""
        from cli import main
        input_csv = tmp_path / "input.csv"
        input_csv.write_text(
            "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
            "T1,KEY-01,12.0,4.0,False,NOMINAL\n"
            "T2,KEY-02,INVALID,15.0,True,DISCORDANT\n",
            encoding="utf-8",
        )
        output_csv = tmp_path / "output.csv"
        result = main(["batch", "-i", str(input_csv), "-o", str(output_csv)])
        assert result == 0
        content = output_csv.read_text(encoding="utf-8")
        # Should have header + 1 valid row (invalid row skipped)
        lines = [l for l in content.strip().split("\n") if l]
        assert len(lines) == 2  # header + 1 data row

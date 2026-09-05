"""
Tests verifying the enrichment suite bug fix (duplicate attribute assignment).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    PedersencommitmentbulletproofsEnrichmentSuite,
    AdditionalEnhancementConfidentialTransactionSimulatorEngine,
    AdditionalEnhancementInnerProductArgumentOptimizerEngine,
)


def test_enrichment_suite_has_distinct_engines():
    """Both confidential tx simulator and inner product optimizer should be present."""
    suite = PedersencommitmentbulletproofsEnrichmentSuite()
    assert hasattr(suite, "confidentialtxsim")
    assert hasattr(suite, "innerproductopt")
    assert isinstance(suite.confidentialtxsim, AdditionalEnhancementConfidentialTransactionSimulatorEngine)
    assert isinstance(suite.innerproductopt, AdditionalEnhancementInnerProductArgumentOptimizerEngine)
    # They must be different instances
    assert suite.confidentialtxsim is not suite.innerproductopt


def test_enrichment_suite_returns_all_8_results():
    """execute_all should return results from all 8 distinct engines."""
    suite = PedersencommitmentbulletproofsEnrichmentSuite()
    results = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(results) == 8
    expected_keys = [
        "PerformanceBenchmarkingSuiteWithOperationCountsAndTimingEngine",
        "SidechannelResistanceAnalysisConstanttimeVerificationEngine",
        "InteroperabilityTestingAgainstLiboqsPqcryptoBoringsslVectorsEngine",
        "ZkProofAggregationForBatchVerificationEngine",
        "FormalSecurityProofDocumentationZeroknowledgeSoundnessEngine",
        "NistComplianceCertificationChecklistWithTestVectorValidationEngine",
        "AdditionalEnhancementConfidentialTransactionSimulatorEngine",
        "AdditionalEnhancementInnerProductArgumentOptimizerEngine",
    ]
    for key in expected_keys:
        assert key in results, f"Missing result key: {key}"


def test_enrichment_suite_distinct_results():
    """Both additional enhancement engines should produce distinct results."""
    suite = PedersencommitmentbulletproofsEnrichmentSuite()
    results = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    tx_result = results["AdditionalEnhancementConfidentialTransactionSimulatorEngine"]
    opt_result = results["AdditionalEnhancementInnerProductArgumentOptimizerEngine"]
    # Both should have the same score (same input) but different feature names
    assert tx_result.score == opt_result.score
    assert tx_result.feature_name != opt_result.feature_name

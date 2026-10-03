"""Unit tests verifying full benchmark evaluation metrics against PRD quality gates."""
import pytest
from pathlib import Path
from src.evaluation.evaluate_all import run_full_evaluation


def test_full_evaluation_gates():
    """Verify that all PRD v1.0 goals and quality gates pass on the complete 150-question benchmark."""
    report_file = Path("docs/evaluation-report.md")
    summary = run_full_evaluation(report_output_path=report_file)

    metrics = summary["overall_metrics"]

    # G1 & G3: Recall@5 >= 85%
    assert metrics["recall_at_5"] >= 0.85, f"Recall@5 ({metrics['recall_at_5']}) below 85%"

    # G3: MRR >= 0.70
    assert metrics["mrr"] >= 0.70, f"MRR ({metrics['mrr']}) below 0.70"

    # G4: Faithfulness >= 90%
    assert metrics["faithfulness"] >= 0.90, f"Faithfulness ({metrics['faithfulness']}) below 90%"

    # G2: Citation correctness >= 90%
    assert metrics["citation_correctness"] >= 0.90, f"Citation Correctness ({metrics['citation_correctness']}) below 90%"

    # G5: Refusal accuracy >= 90%
    assert metrics["refusal_accuracy"] >= 0.90, f"Refusal Accuracy ({metrics['refusal_accuracy']}) below 90%"

    # False refusal rate <= 15%
    assert metrics["false_refusal_rate"] <= 0.15, f"False Refusal Rate ({metrics['false_refusal_rate']}) exceeds 15%"

    # G6: p95 latency under 8 seconds
    assert metrics["p95_latency_seconds"] < 8.0, f"Latency ({metrics['p95_latency_seconds']}s) exceeds 8s"

    # G8: Check Odia within 10 percentage points of English
    en_r5 = summary["per_language"]["en"]["recall_at_5"]
    or_r5 = summary["per_language"]["or"]["recall_at_5"]
    gap = abs(en_r5 - or_r5) * 100
    assert gap <= 10.0, f"Odia Recall@5 gap ({gap:.1f}%) exceeds 10 percentage points from English"

    # Report file exists and is populated
    assert report_file.exists()
    assert report_file.stat().st_size > 500

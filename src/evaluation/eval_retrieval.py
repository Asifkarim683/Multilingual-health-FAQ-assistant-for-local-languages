"""Retrieval evaluation runner computing Recall@k and Mean Reciprocal Rank (MRR)."""
import csv
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
import json

from src.retrieval.vector_store import VectorStore


def evaluate_retrieval(
    eval_csv_path: Path = Path("data/eval/questions_draft.csv"),
    chunks_path: Path = Path("data/processed/chunks.json"),
    k: int = 5,
) -> Dict[str, Any]:
    """Evaluate vector search recall and MRR across test set."""
    if not eval_csv_path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {eval_csv_path}")

    # Load vector store
    store = VectorStore.from_processed_chunks(chunks_path)

    # Read questions
    questions = []
    with open(eval_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)

    total_by_lang = defaultdict(int)
    recall_at_1_by_lang = defaultdict(int)
    recall_at_k_by_lang = defaultdict(int)
    mrr_sum_by_lang = defaultdict(float)

    total_queries = len(questions)
    total_recall_at_1 = 0
    total_recall_at_k = 0
    total_mrr_sum = 0.0

    detailed_results = []

    for item in questions:
        lang = item["language"]
        q_text = item["question"]
        gold_src = item["gold_source_id"]

        results = store.search(q_text, top_k=k, lang_filter=lang)
        retrieved_sources = [r.source_id.split("-")[0] + ("-" + r.source_id.split("-")[1] if len(r.source_id.split("-")) > 1 and r.source_id.split("-")[1].isdigit() else "") for r in results]
        # Clean source prefix matching: e.g. SRC-01 matches SRC-01 or SRC-01-HI or SRC-01-OR
        matched_rank = None
        for rank, r in enumerate(results, 1):
            if r.source_id.startswith(gold_src):
                matched_rank = rank
                break

        total_by_lang[lang] += 1

        is_hit_at_1 = matched_rank == 1
        is_hit_at_k = matched_rank is not None and matched_rank <= k
        rr = 1.0 / matched_rank if matched_rank is not None else 0.0

        if is_hit_at_1:
            total_recall_at_1 += 1
            recall_at_1_by_lang[lang] += 1

        if is_hit_at_k:
            total_recall_at_k += 1
            recall_at_k_by_lang[lang] += 1

        total_mrr_sum += rr
        mrr_sum_by_lang[lang] += rr

        detailed_results.append({
            "id": item["id"],
            "language": lang,
            "question": q_text,
            "gold_source": gold_src,
            "matched_rank": matched_rank,
            "reciprocal_rank": rr,
            "top_retrieved": [r.source_id for r in results],
        })

    summary = {
        "total_queries": total_queries,
        "k": k,
        "overall_recall_at_1": round(total_recall_at_1 / total_queries, 4),
        "overall_recall_at_k": round(total_recall_at_k / total_queries, 4),
        "overall_mrr": round(total_mrr_sum / total_queries, 4),
        "per_language": {},
    }

    for lang in total_by_lang:
        n = total_by_lang[lang]
        summary["per_language"][lang] = {
            "count": n,
            f"recall_at_1": round(recall_at_1_by_lang[lang] / n, 4),
            f"recall_at_{k}": round(recall_at_k_by_lang[lang] / n, 4),
            "mrr": round(mrr_sum_by_lang[lang] / n, 4),
        }

    # Print Report
    print("=" * 65)
    print(f"RETRIEVAL EVALUATION REPORT (k={k})")
    print("=" * 65)
    print(f"Total Questions Evaluated: {total_queries}")
    print(f"Overall Recall@{k}       : {summary['overall_recall_at_k'] * 100:.1f}%")
    print(f"Overall Recall@1       : {summary['overall_recall_at_1'] * 100:.1f}%")
    print(f"Overall MRR            : {summary['overall_mrr']:.3f}")
    print("-" * 65)
    print("Per-Language Breakdown:")
    for lang, metrics in summary["per_language"].items():
        print(
            f"  {lang.upper():5s} | Qs: {metrics['count']:2d} | "
            f"Recall@{k}: {metrics[f'recall_at_{k}'] * 100:5.1f}% | "
            f"MRR: {metrics['mrr']:.3f}"
        )
    print("=" * 65)

    # Save summary report
    report_file = Path("data/eval/retrieval_baseline_report.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary


if __name__ == "__main__":
    evaluate_retrieval()

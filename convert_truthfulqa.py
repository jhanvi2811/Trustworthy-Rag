import csv
import json
from pathlib import Path

input_file = Path("data/raw/truthfulqa/TruthfulQA.csv")
output_file = Path("data/raw/truthfulqa/truthfulqa.jsonl")

if not input_file.exists():
    raise FileNotFoundError(f"CSV not found: {input_file}")

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(input_file, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    print("CSV columns:")
    print(reader.fieldnames)

    # Find columns case-insensitively
    columns = {c.strip().lower(): c for c in reader.fieldnames or []}

    question_col = columns.get("question")
    best_answer_col = columns.get("best answer") or columns.get("best_answer")

    if not question_col or not best_answer_col:
        raise ValueError(
            "\nCould not find required columns.\n"
            f"Available columns: {reader.fieldnames}\n"
            "Expected: Question and Best Answer"
        )

    count = 0

    with open(output_file, "w", encoding="utf-8") as out:
        for row in reader:
            question = (row.get(question_col) or "").strip()
            best_answer = (row.get(best_answer_col) or "").strip()

            if not question or not best_answer:
                continue

            record = {
                "question": question,
                "best_answer": best_answer
            }

            out.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            count += 1

print("\nConversion complete.")
print(f"Created: {output_file}")
print(f"Total samples: {count}")
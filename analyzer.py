from collections import Counter
import string

import pandas as pd

SAMPLE_TEXT = (
    "Data visualization helps people understand patterns quickly. "
    "This sample paragraph gives the analyzer enough English letters "
    "to show a more meaningful frequency distribution."
)


def build_frequency_table(text: str) -> tuple[pd.DataFrame, int]:
    normalized = text.lower()
    letters = [char for char in normalized if char in string.ascii_lowercase]
    counter = Counter(letters)
    total_letters = len(letters)

    rows = []
    for letter in string.ascii_lowercase:
        count = counter.get(letter, 0)
        frequency = count / total_letters if total_letters else 0
        rows.append(
            {
                "Letter": letter.upper(),
                "Count": count,
                "Frequency": frequency,
            }
        )

    data = pd.DataFrame(rows).sort_values(
        by=["Frequency", "Count", "Letter"],
        ascending=[False, False, True],
        ignore_index=True,
    )
    return data, total_letters


def build_summary(text: str) -> dict[str, int]:
    total_chars = len(text)
    total_letters = sum(1 for char in text.lower() if char in string.ascii_lowercase)
    return {
        "total_chars": total_chars,
        "total_letters": total_letters,
        "is_empty": int(not text.strip()),
    }


def build_export_csv(data: pd.DataFrame) -> str:
    export_df = data[["Letter", "Count", "Frequency"]].copy()
    return export_df.to_csv(index=False)


def build_result_insights(data: pd.DataFrame, total_letters: int) -> dict[str, object]:
    top_three = data.head(3)[["Letter", "Frequency"]].to_dict("records")
    non_zero_letters = int((data["Count"] > 0).sum())
    return {
        "top_three": top_three,
        "short_sample": total_letters < 30,
        "sparse_distribution": non_zero_letters <= 5,
    }

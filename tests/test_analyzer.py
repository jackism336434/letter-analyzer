import pandas as pd

from analyzer import (
    build_export_csv,
    build_frequency_table,
    build_result_insights,
    build_summary,
)


def test_build_summary_for_empty_text() -> None:
    summary = build_summary("   ")

    assert summary["is_empty"] == 1
    assert summary["total_chars"] == 3
    assert summary["total_letters"] == 0


def test_build_frequency_table_for_non_english_input() -> None:
    data, total_letters = build_frequency_table("12345 !@#")

    assert total_letters == 0
    assert len(data) == 26
    assert int(data["Count"].sum()) == 0
    assert float(data["Frequency"].sum()) == 0.0


def test_build_frequency_table_counts_letters_correctly() -> None:
    data, total_letters = build_frequency_table("banana")

    assert total_letters == 6
    assert data.iloc[0]["Letter"] == "A"
    assert data.iloc[0]["Count"] == 3
    assert data.iloc[1]["Letter"] == "N"
    assert data.iloc[1]["Count"] == 2


def test_build_result_insights_marks_short_sample() -> None:
    data, total_letters = build_frequency_table("short sample")
    insights = build_result_insights(data, total_letters)

    assert insights["short_sample"] is True
    assert len(insights["top_three"]) == 3


def test_build_export_csv_contains_expected_columns() -> None:
    data, _ = build_frequency_table("abcabc")
    csv_output = build_export_csv(data)
    exported = pd.read_csv(pd.io.common.StringIO(csv_output))

    assert list(exported.columns) == ["Letter", "Count", "Frequency"]

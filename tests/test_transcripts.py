import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from knowledge_base import load_all_records
from parser import parse_transcript


FILES = [
    "Transcript_1_France.txt",
    "Transcript_2_Germany.txt",
    "Transcript_3_UK.txt",
]


def test_each_transcript_has_expected_metadata_and_records():
    records = [parse_transcript(filename) for filename in FILES]

    assert [len(items) for items in records] == [14, 14, 14]
    assert [items[0]["market"] for items in records] == [
        "France",
        "Germany",
        "United Kingdom",
    ]
    assert [items[0]["expert"] for items in records] == [
        "Dr. Jean Martin",
        "Anna Keller",
        "Dr. Emily Carter",
    ]
    assert all(item["timestamp"] for items in records for item in items)


def test_knowledge_base_contains_expert_and_interviewer_records():
    records = load_all_records()

    assert len(records) == 42
    assert {record["speaker"] for record in records} >= {"Interviewer"}
    assert sum(record["speaker"] != "Interviewer" for record in records) == 21
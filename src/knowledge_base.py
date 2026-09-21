from parser import parse_transcript


TRANSCRIPT_FILES = [
    "Transcript_1_France.txt",
    "Transcript_2_Germany.txt",
    "Transcript_3_UK.txt",
]


def load_all_records():
    all_records = []

    for filename in TRANSCRIPT_FILES:
        records = parse_transcript(filename)
        all_records.extend(records)

    return all_records


if __name__ == "__main__":

    records = load_all_records()

    print("=" * 70)
    print("KNOWLEDGE BASE")
    print("=" * 70)

    print(f"Total records: {len(records)}")

    print("\nMarkets:")

    markets = {}

    for record in records:
        market = record["market"]
        markets[market] = markets.get(market, 0) + 1

    for market, count in markets.items():
        print(f"{market}: {count} records")

    print("\nExample record:")
    print(records[1])
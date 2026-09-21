from pathlib import Path
import re


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_transcript(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Transcript not found: {file_path}")

    return file_path.read_text(encoding="utf-8")


def parse_transcript(filename):
    text = load_transcript(filename)

    lines = text.splitlines()

    # Extract basic expert information
    expert_match = re.search(r"Expert \d+ – (.+)", text)
    role_match = re.search(r"Role: (.+)", text)
    market_match = re.search(r"Market: (.+)", text)

    expert = expert_match.group(1).strip() if expert_match else "Unknown"
    role = role_match.group(1).strip() if role_match else "Unknown"
    market = market_match.group(1).strip() if market_match else "Unknown"

    records = []

    current_timestamp = None
    current_speaker = None
    current_text = []

    timestamp_pattern = re.compile(r"^\d{2}:\d{2}$")

    def save_record():
        if current_timestamp and current_text:
            full_text = " ".join(current_text).strip()

            records.append({
                "expert": expert,
                "role": role,
                "market": market,
                "timestamp": current_timestamp,
                "speaker": current_speaker,
                "text": full_text
            })

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # New timestamp
        if timestamp_pattern.match(line):
            save_record()

            current_timestamp = line
            current_speaker = None
            current_text = []

        else:
            # First line after timestamp contains speaker + text
            if current_timestamp and current_speaker is None:

                if ":" in line:
                    speaker, content = line.split(":", 1)

                    current_speaker = speaker.strip()
                    current_text = [content.strip()]
                else:
                    current_text = [line]

            elif current_timestamp:
                current_text.append(line)

    # Save final record
    save_record()

    return records


if __name__ == "__main__":

    files = [
        "Transcript_1_France.txt",
        "Transcript_2_Germany.txt",
        "Transcript_3_UK.txt",
    ]

    for filename in files:

        print("\n" + "=" * 70)
        print(filename)
        print("=" * 70)

        records = parse_transcript(filename)

        print(f"Records extracted: {len(records)}")

        for record in records[:3]:
            print(record)
from pathlib import Path
import os

from dotenv import load_dotenv

try:
    from google import genai
except ImportError:  # The dependency is installed from requirements.txt.
    genai = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key and genai else None


def generate_answer(prompt):
    if genai is None:
        raise RuntimeError("google-genai is not installed.")
    if not api_key or client is None:
        raise RuntimeError(
            "Gemini is not configured. Set GEMINI_API_KEY in the environment."
        )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    answer = response.text
    if not answer or not answer.strip():
        raise RuntimeError("Gemini returned an empty response.")

    return answer.strip()
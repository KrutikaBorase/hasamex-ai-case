import sys
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parent))

from knowledge_base import load_all_records


MODEL_NAME = "all-MiniLM-L6-v2"


class TranscriptRetriever:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

        print("Loading transcript records...")
        self.records = load_all_records()

        # Only index expert responses
        self.expert_records = [
            record
            for record in self.records
            if record["speaker"] != "Interviewer"
        ]

        texts = [
            record["text"]
            for record in self.expert_records
        ]

        print(f"Creating embeddings for {len(texts)} expert responses...")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings.astype("float32"))

        print("Vector index ready.")

    def search(self, query, top_k=5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            record = self.expert_records[index].copy()

            record["score"] = float(score)

            results.append(record)

        return results


if __name__ == "__main__":

    retriever = TranscriptRetriever()

    query = "What are the main barriers to robotic surgery adoption?"

    results = retriever.search(query, top_k=5)

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 70)
        print(f"Market: {result['market']}")
        print(f"Expert: {result['expert']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Score: {result['score']:.4f}")
        print(f"Text: {result['text']}")
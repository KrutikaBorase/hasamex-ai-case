from retriever import TranscriptRetriever
from llm import generate_answer


class CrossCallAnalyzer:

    def __init__(self):
        self.retriever = TranscriptRetriever()

    def analyze(self, question, top_k=10):

        results = self.retriever.search(
            question,
            top_k=top_k
        )

        evidence_blocks = []

        for result in results:
            evidence_blocks.append(
                f"""
Market: {result['market']}
Expert: {result['expert']}
Role: {result['role']}
Timestamp: {result['timestamp']}
Exact transcript text: {result['text']}
"""
            )

        evidence = "\n---\n".join(evidence_blocks)

        prompt = f"""
You are a qualitative market research analyst.

Analyze the following expert interview evidence.

Question:
{question}

Evidence from the interviews:
{evidence}

Your task:

1. Identify the common themes across the three markets.
2. Identify meaningful differences between the markets.
3. Do not call something a disagreement unless the evidence actually
   shows different views or emphasis.
4. Do not invent information.
5. Do not invent quotes, experts, markets, or timestamps.
6. Use only the supplied transcript evidence.
7. Clearly separate common themes from differences.
8. Do not provide citations, quotes, timestamps, expert names, or market names
    in the analytical synthesis. Python will render the source evidence separately.
9. If there is insufficient evidence, say:
    "Insufficient evidence in the provided transcripts."

Return the analysis in this structure:

## Common Themes

- Theme 1
- Theme 2
- Theme 3

## Differences Across Markets

- Difference 1
- Difference 2

"""

        answer = generate_answer(prompt)

        return {
            "question": question,
            "answer": answer,
            "retrieved_records": results,
        }


if __name__ == "__main__":

    analyzer = CrossCallAnalyzer()

    question = """
    What are the common themes and differences across France,
    Germany, and the United Kingdom regarding robotic surgery
    adoption and purchasing?
    """

    result = analyzer.analyze(question)

    print("\n" + "=" * 70)
    print("CROSS-CALL ANALYSIS")
    print("=" * 70)

    print(result["answer"])
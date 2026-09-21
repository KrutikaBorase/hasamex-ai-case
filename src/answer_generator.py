from retriever import TranscriptRetriever
from llm import generate_answer


class AnswerGenerator:

    def __init__(self):
        self.retriever = TranscriptRetriever()

    def answer_question(self, question, top_k=7):

        results = self.retriever.search(
            question,
            top_k=top_k
        )

        evidence_blocks = []

        for i, result in enumerate(results, start=1):
            evidence_blocks.append(
                f"""
Evidence {i}

Market: {result['market']}
Expert: {result['expert']}
Role: {result['role']}
Timestamp: {result['timestamp']}
Transcript text: {result['text']}
"""
            )

        evidence = "\n---\n".join(evidence_blocks)

        prompt = f"""
You are a qualitative market research analyst.

Answer this interview question using ONLY the transcript evidence below.

Question:
{question}

Evidence:
{evidence}

Instructions:
- Synthesize the evidence across the European markets.
- Identify important similarities and differences when supported.
- Do not invent facts.
- Do not invent information that is not present in the evidence.
- Do not generate quotes.
- Do not generate timestamps.
- Do not generate expert names or market names.
- Do not create a separate evidence section.
- Keep the answer concise and business-focused.
- If the evidence is insufficient, say:
  "Insufficient evidence in the provided transcripts."

Return ONLY the analytical synthesis.
"""

        answer = generate_answer(prompt)

        return {
            "question": question,
            "answer": answer,
            "retrieved_records": results,
        }


if __name__ == "__main__":

    generator = AnswerGenerator()

    question = "What are the main barriers to adoption?"

    result = generator.answer_question(question)

    print("\n" + "=" * 70)
    print("INTERVIEW GUIDE ANSWER")
    print("=" * 70)

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\n" + "=" * 70)
    print("SOURCE EVIDENCE")
    print("=" * 70)

    for record in result["retrieved_records"]:

        print(
            f"\n{record['market']} | "
            f"{record['expert']} | "
            f"{record['timestamp']}"
        )

        print(record["text"])
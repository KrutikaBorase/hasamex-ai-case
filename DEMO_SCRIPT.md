# Demo Script

## 1. Introduction — 20 seconds

This is the Hasamex qualitative research application. It analyzes three expert interviews about robotic surgery adoption in France, Germany, and the United Kingdom.

The key design choice is grounding: Gemini writes the synthesis, but Python controls the quotes, timestamps, and expert metadata.

## 2. Interview Guide — 45 seconds

I’ll open **Interview Guide** and select a question, for example, “What are the main barriers to adoption?”

After clicking **Generate Answer**, the app retrieves expert responses and sends only that evidence to Gemini. The answer is the analytical synthesis.

I’ll expand a supporting evidence item. This shows the market, expert, role, timestamp, and the exact quote copied from the original transcript.

## 3. Ask Across Calls — 30 seconds

Next, **Ask Across Calls** allows a custom question, such as how important budgets and ROI are in purchasing decisions.

The answer is synthesized across the interviews, while the supporting evidence remains separately visible and traceable.

## 4. Cross-Call Analysis — 35 seconds

**Cross-Call Analysis** compares all three markets. It asks Gemini to identify common themes and meaningful differences, but not unsupported disagreements.

The evidence list below is attached by Python, so the model does not control the displayed timestamps or citations.

## 5. Transcript Explorer — 30 seconds

Finally, **Transcript Explorer** is the validation view. I can filter by market and expert, then inspect every timestamped interviewer and expert record in chronological order.

This makes it possible to verify any AI-generated synthesis against the original source wording.

## 6. Closing — 20 seconds

The architecture is: transcripts to parser, knowledge base, embeddings, FAISS retrieval, grounded Gemini synthesis, and Streamlit display. This keeps the application simple while prioritizing factual grounding and source traceability.

import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PATH SETUP
# ============================================================

SRC_DIR = Path(__file__).resolve().parent / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from interview_guide import get_questions
from answer_generator import AnswerGenerator
from knowledge_base import load_all_records
from cross_call_analysis import CrossCallAnalyzer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="European Robotic Surgery Market",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 European Robotic Surgery Market")
st.caption(
    "AI-powered analysis of expert interviews across France, Germany and the UK"
)


# ============================================================
# LOAD AI GENERATOR
# ============================================================

@st.cache_resource
def load_generator():
    return AnswerGenerator()


@st.cache_resource
def load_cross_call_analyzer():
    return CrossCallAnalyzer()


# Create generator
generator = load_generator()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Interview Guide",
        "Ask Across Calls",
        "Cross-Call Analysis",
        "Transcript Explorer",
    ]
)


# ============================================================
# PAGE 1 — INTERVIEW GUIDE
# ============================================================

if page == "Interview Guide":

    st.header("📋 Interview Guide")

    st.write(
        "Select a question from the interview guide. "
        "The application retrieves relevant expert responses "
        "and generates a concise synthesis."
    )

    questions = get_questions()

    selected_question = st.selectbox(
        "Select an interview question",
        questions
    )

    if st.button(
        "Generate Answer",
        type="primary"
    ):

        try:
            with st.spinner(
                "Searching transcripts and generating answer..."
            ):
                result = generator.answer_question(
                    selected_question,
                    top_k=7
                )
        except Exception:
            st.error(
                "Unable to generate an answer. Check the Gemini configuration "
                "and application dependencies."
            )
            st.stop()

        # ----------------------------------------------------
        # GENERATED ANSWER
        # ----------------------------------------------------

        st.subheader("Answer")

        st.write(
            result["answer"]
        )

        # ----------------------------------------------------
        # SUPPORTING EVIDENCE
        # ----------------------------------------------------

        st.subheader("Supporting Evidence")

        st.caption(
            "Quotes, timestamps and expert metadata are taken "
            "directly from the source transcripts."
        )

        for i, record in enumerate(
            result["retrieved_records"],
            start=1
        ):

            with st.expander(
                f"{i}. {record['market']} — "
                f"{record['expert']} — "
                f"{record['timestamp']}"
            ):

                st.markdown(
                    f"**Market:** {record['market']}"
                )

                st.markdown(
                    f"**Expert:** {record['expert']}"
                )

                st.markdown(
                    f"**Role:** {record['role']}"
                )

                st.markdown(
                    f"**Timestamp:** `{record['timestamp']}`"
                )

                st.markdown(
                    "**Exact Quote:**"
                )

                st.info(
                    record["text"]
                )

                st.caption(
                    f"Semantic relevance score: "
                    f"{record['score']:.4f}"
                )


# ============================================================
# PAGE 2 — ASK ACROSS CALLS
# ============================================================

elif page == "Ask Across Calls":

    st.header("🌍 Ask Across Calls")

    st.write(
        "Ask a custom question and analyze information "
        "across the three expert interviews."
    )

    question = st.text_input(
        "Ask a question about the three expert interviews",
        placeholder=(
            "Example: How important is ROI in purchasing decisions?"
        )
    )

    ask_clicked = st.button(
        "Ask",
        type="primary",
        key="ask_across_calls_button"
    )

    if ask_clicked and question.strip():

        try:
            with st.spinner(
                "Searching interviews and generating answer..."
            ):
                result = generator.answer_question(
                    question,
                    top_k=7
                )
        except Exception:
            st.error(
                "Unable to generate an answer. Check the Gemini configuration "
                "and application dependencies."
            )
            st.stop()

        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        st.subheader("Answer")

        st.write(
            result["answer"]
        )

        # ----------------------------------------------------
        # SOURCE EVIDENCE
        # ----------------------------------------------------

        st.subheader("Supporting Evidence")

        st.caption(
            "The following evidence was retrieved directly "
            "from the expert transcripts."
        )

        for i, record in enumerate(
            result["retrieved_records"],
            start=1
        ):

            with st.expander(
                f"{i}. {record['market']} — "
                f"{record['expert']} — "
                f"{record['timestamp']}"
            ):

                st.markdown(
                    f"**Market:** {record['market']}"
                )

                st.markdown(
                    f"**Expert:** {record['expert']}"
                )

                st.markdown(
                    f"**Role:** {record['role']}"
                )

                st.markdown(
                    f"**Timestamp:** `{record['timestamp']}`"
                )

                st.markdown(
                    "**Exact Quote:**"
                )

                st.info(
                    record["text"]
                )

                st.caption(
                    f"Semantic relevance score: "
                    f"{record['score']:.4f}"
                )

    elif ask_clicked:
        st.warning(
            "Please enter a question first."
        )


# ============================================================
# PAGE 3 — CROSS-CALL ANALYSIS
# ============================================================

elif page == "Cross-Call Analysis":

    st.header("🔎 Cross-Call Analysis")
    st.write(
        "Compare common themes and market-specific differences using "
        "expert evidence from all three interviews."
    )

    if st.button(
        "Analyze All Calls",
        type="primary",
        key="analyze_all_calls_button"
    ):
        try:
            with st.spinner("Comparing expert interviews..."):
                result = load_cross_call_analyzer().analyze(
                    "What are the common themes and meaningful differences "
                    "in robotic surgery adoption across the three markets?",
                    top_k=10,
                )
        except Exception:
            st.error(
                "Unable to analyze the interviews. Check the Gemini configuration "
                "and application dependencies."
            )
            st.stop()

        st.subheader("Analysis")
        st.write(result["answer"])
        st.subheader("Source Evidence")
        st.caption(
            "Evidence below is attached by Python from the original transcripts."
        )

        for i, record in enumerate(result["retrieved_records"], start=1):
            with st.expander(
                f"{i}. {record['market']} — {record['expert']} — "
                f"{record['timestamp']}"
            ):
                st.markdown(f"**Market:** {record['market']}")
                st.markdown(f"**Expert:** {record['expert']}")
                st.markdown(f"**Role:** {record['role']}")
                st.markdown(f"**Timestamp:** `{record['timestamp']}`")
                st.markdown("**Exact Quote:**")
                st.info(record["text"])
                st.caption(f"Semantic relevance score: {record['score']:.4f}")


# ============================================================
# PAGE 4 — TRANSCRIPT EXPLORER
# ============================================================

elif page == "Transcript Explorer":

    st.header("📚 Transcript Explorer")

    st.write(
        "Browse the original expert interview evidence "
        "by market, expert and timestamp."
    )

    # --------------------------------------------------------
    # LOAD ALL RECORDS
    # --------------------------------------------------------

    records = load_all_records()

    # --------------------------------------------------------
    # MARKET FILTER
    # --------------------------------------------------------

    markets = sorted(
        list(
            set(
                record["market"]
                for record in records
            )
        )
    )

    selected_market = st.selectbox(
        "Select market",
        markets
    )

    # --------------------------------------------------------
    # FILTER BY MARKET
    # --------------------------------------------------------

    market_records = [
        record
        for record in records
        if record["market"] == selected_market
    ]

    # --------------------------------------------------------
    # EXPERT FILTER
    # --------------------------------------------------------

    experts = sorted(
        list(
            set(
                record["expert"]
                for record in market_records
            )
        )
    )

    selected_expert = st.selectbox(
        "Select expert",
        experts
    )

    # --------------------------------------------------------
    # FILTER BY EXPERT
    # --------------------------------------------------------

    expert_records = [
        record
        for record in market_records
        if record["expert"] == selected_expert
    ]

    # --------------------------------------------------------
    # EXPERT INFORMATION
    # --------------------------------------------------------

    st.subheader(
        f"{selected_expert} — {selected_market}"
    )

    if expert_records:

        first_record = expert_records[0]

        st.markdown(
            f"**Role:** {first_record['role']}"
        )

        st.markdown(
            f"**Market:** {first_record['market']}"
        )

        st.divider()

    # --------------------------------------------------------
    # DISPLAY TRANSCRIPT
    # --------------------------------------------------------

    for record in expert_records:

        with st.expander(
            f"{record['timestamp']} — "
            f"{record['speaker']}"
        ):

            st.markdown(
                f"**Timestamp:** `{record['timestamp']}`"
            )

            st.markdown(
                f"**Speaker:** {record['speaker']}"
            )

            st.markdown(
                "**Exact transcript:**"
            )

            st.info(
                record["text"]
            )
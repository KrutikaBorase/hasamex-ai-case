INTERVIEW_QUESTIONS = [
    "How would you describe current adoption of robotic surgery in your market?",
    "What are the main barriers to adoption?",
    "How important are hospital budgets and ROI in purchasing decisions?",
    "How important are surgeon training and clinical outcomes?",
    "What adoption trend do you expect over the next 3–5 years?",
    "What is the typical hospital decision-making timeline for purchasing a new robotic system?",
]


def get_questions():
    return INTERVIEW_QUESTIONS


if __name__ == "__main__":
    for number, question in enumerate(INTERVIEW_QUESTIONS, start=1):
        print(f"{number}. {question}")
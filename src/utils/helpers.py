import os
from datetime import datetime
import streamlit as st
import pandas as pd
from src.generator.question_generator import Question_generator
from src.common.logger import get_logger
from src.config.settings import settings

def rerun():
    st.session_state['rerun_trigger'] = not st.session_state.get("rerun_trigger", False)
    # trigger streamlit to reload or rerun

class QuizManager:
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.results = []
        self.logger = get_logger(self.__class__.__name__)

    def generate_questions(self, generator: Question_generator, topic: str, question_type: str, difficulty: str, number_of_questions: int):
        self.questions = []
        self.user_answers = []
        self.results = []
        try:
            for _ in range(number_of_questions):
                if question_type == "Multiple Choice":
                    question = generator.generate_mcq(topic, difficulty.lower())
                    self.questions.append({
                        "type": "MCQ",
                        "question": question.question,
                        "options": question.options,
                        "correct_answer": question.correct_answer
                    })
                else:
                    question = generator.generate_fill_blank(topic, difficulty.lower())
                    self.questions.append({
                        "type": "fill in the blanks",
                        "question": question.question,
                        "correct_answer": question.answer
                    })
        except Exception as e:
            self.logger.error(f"Error generating question: {e}")
            st.error(f"Error generating question: {e}")
            return False
        return True
    def attempt_quiz(self):
        self.user_answers = []
        for i, q in enumerate(self.questions):
            st.markdown(f"**Question {i + 1}: {q['question']}**")
            if q['type'] == 'MCQ':
                user_answer = st.radio(
                    f"Select an answer for Question {i + 1}",
                    q['options'],
                    key=f"mcq_{i}"
                )
            else:
                user_answer = st.text_input(
                    f"Fill in the blank for Question {i + 1}",
                    key=f"fill_blank_{i}"
                )
            self.user_answers.append(user_answer)

    def evaluate_quiz(self):
        self.results = []
        for i, (q, user_ans) in enumerate(zip(self.questions, self.user_answers)):
            is_correct = False
            if q['type'] == 'MCQ':
                is_correct = user_ans == q['correct_answer']
            else:
                is_correct = user_ans.strip().lower() == q['correct_answer'].strip().lower()
            self.results.append({
                "question_number": i + 1,
                "question": q['question'],
                "question_type": q['type'],
                "options": q.get('options', []),
                "user_answer": user_ans,
                "correct_answer": q['correct_answer'],
                "is_correct": is_correct
            })

    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)

    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.warning("No results to save!")
            return None
        df = self.generate_result_dataframe()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = getattr(settings, "RESULTS_DIR", "results")
        os.makedirs(results_dir, exist_ok=True)
        unique_filename = f"{filename_prefix}_{timestamp}.csv"
        full_path = os.path.join(results_dir, unique_filename)
        try:
            df.to_csv(full_path, index=False)
            st.success("Results saved successfully.")
            self.logger.info(f"Results saved to {full_path}")
            return full_path
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            st.error(f"Failed to save results: {e}")
            return None

import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import Question_generator
load_dotenv()


def main():
    st.set_page_config(page_title="Study Buddy AI", page_icon="🎧")
    
    # Check for API key at startup
    from src.config.settings import settings
    
    # Try to get API key from multiple sources
    api_key = None
    
    # First check environment variable
    api_key = os.getenv("GROQ_API_KEY")
    
    # If not found, try Streamlit secrets directly
    if not api_key:
        try:
            # Try to access Streamlit secrets
            if hasattr(st, 'secrets') and st.secrets is not None:
                try:
                    api_key = st.secrets.get("GROQ_API_KEY", None)
                    if not api_key:
                        # Try direct dictionary access
                        api_key = st.secrets.get("GROQ_API_KEY") or getattr(st.secrets, "GROQ_API_KEY", None)
                except Exception:
                    pass
        except Exception:
            pass
    
    # If still not found, try from settings (which also checks secrets)
    if not api_key:
        api_key = settings.GROQ_API_KEY
    
    if not api_key:
        st.error("⚠️ **API Key Missing**")
        st.markdown("""
        The Groq API key is not configured. Please set the `GROQ_API_KEY` environment variable.
        
        **For Streamlit Cloud:**
        1. Go to your app settings (click the **three dots (⋮)** menu in the top right)
        2. Click on **"Settings"** or **"Manage app"**
        3. Click on **"Secrets"** in the left sidebar
        4. Add the following in **TOML format** (exactly as shown):
        ```toml
        GROQ_API_KEY = "your_actual_api_key_here"
        ```
        5. Click **"Save"** - the app will automatically redeploy
        
        **Important Notes:**
        - Use **quotes** around your API key value
        - Use **TOML format** (not plain text)
        - Make sure there are **no extra spaces** before or after the `=`
        - The key name must be exactly: `GROQ_API_KEY`
        
        **For Local Development:**
        Create a `.env` file in the project root with:
        ```
        GROQ_API_KEY=your_api_key_here
        ```
        """)
        st.stop()

    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger' not in st.session_state:
        st.session_state.rerun_trigger = False
        

    st.title("Study Buddy AI")

    st.sidebar.header("Quiz Settings")

    question_type = st.sidebar.selectbox(
        "Select Question Type" ,
        ["Multiple Choice" , "Fill in the Blank"],
        index=0
    )

    topic = st.sidebar.text_input("Enter Topic", placeholder="Indian History, geography")

    difficulty = st.sidebar.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"],
        index=1
    )

    num_questions=st.sidebar.number_input(
        "Number of Questions",
        min_value=1,  max_value=10 , value=5
    )

    

    
    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False

        generator = Question_generator()
        success = st.session_state.quiz_manager.generate_questions(
            generator,
            topic,question_type,difficulty,num_questions
        )

        st.session_state.quiz_generated = success
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count/total_questions)*100
            st.write(f"Score : {score_percentage}")

            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.success(f"✅ Question {question_num} : {result['question']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                    st.write(f"Correct answer : {result['correct_answer']}")
                
                st.markdown("-------")

            
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file,'rb') as f:
                        st.download_button(
                            label="Download Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime='text/csv'
                        )
                else:
                    st.warning("No results available")

if __name__=="__main__":
    main()

        
# AI Study Buddy

An intelligent quiz generation application powered by AI to help students study and test their knowledge.

## Features

- Generate multiple-choice questions
- Generate fill-in-the-blank questions
- Customizable difficulty levels (Easy, Medium, Hard)
- Interactive quiz interface
- Automatic quiz evaluation
- Export results to CSV

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

3. Run the application:
```bash
streamlit run application.py
```

### Streamlit Cloud Deployment

1. Push your code to GitHub (already done ✅)

2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your repository

3. **Important**: Add your Groq API key as a secret:
   - In your Streamlit Cloud app, click the **three dots (⋮)** menu in the top right
   - Select **"Settings"** or **"Manage app"**
   - Click on **"Secrets"** in the left sidebar
   - Paste the following (replace with your actual API key):
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```
   - **Important**: Use TOML format with quotes around the value
   - Click **"Save"** - the app will automatically redeploy

4. Deploy your app!

**Note**: The app will show a helpful error message if the API key is not configured.

## Usage

1. Select question type (Multiple Choice or Fill in the Blank)
2. Enter a topic
3. Choose difficulty level
4. Set number of questions
5. Click "Generate Quiz"
6. Answer the questions
7. Submit and view results
8. Download results as CSV

## Technologies

- Python
- Streamlit
- LangChain
- Groq API
- Pandas

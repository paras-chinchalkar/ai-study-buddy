# Streamlit Cloud Setup Guide

## Adding Your Groq API Key to Streamlit Cloud

### Step-by-Step Instructions:

1. **Open Your App in Streamlit Cloud**
   - Go to https://share.streamlit.io or your Streamlit Cloud dashboard
   - Find your app and open it

2. **Access App Settings**
   - Click the **three dots (⋮)** menu in the **top right corner** of your app
   - Select **"Settings"** or **"Manage app"** from the dropdown

3. **Navigate to Secrets**
   - In the left sidebar, click on **"Secrets"**
   - You'll see a text editor for secrets

4. **Add Your API Key**
   - In the secrets editor, paste the following (replace with your actual API key):
   ```toml
   GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
   ```
   
   **Important Formatting:**
   - ✅ Use **quotes** around the value: `"your_key"`
   - ✅ Use **TOML format** (not plain text)
   - ✅ No spaces around the `=` sign
   - ✅ Key name must be exactly: `GROQ_API_KEY`

5. **Save**
   - Click the **"Save"** button
   - Streamlit Cloud will automatically redeploy your app

6. **Verify**
   - Wait for the app to redeploy (usually takes 30-60 seconds)
   - Refresh your app page
   - The error message should disappear and the app should work

### Common Mistakes to Avoid:

❌ **Wrong Format:**
```toml
GROQ_API_KEY=your_key_here          # Missing quotes
GROQ_API_KEY = your_key_here        # Missing quotes
GROQ_API_KEY = " your_key_here "    # Extra spaces inside quotes
```

✅ **Correct Format:**
```toml
GROQ_API_KEY = "your_key_here"      # Perfect!
```

### Getting Your Groq API Key:

1. Go to https://console.groq.com/
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key or copy an existing one
5. Copy the key (it starts with `gsk_`)

### Troubleshooting:

- **Still seeing the error?** 
  - Make sure you saved the secrets
  - Wait for the app to redeploy (check the deployment status)
  - Verify the key name is exactly `GROQ_API_KEY` (case-sensitive)
  - Make sure there are quotes around the value

- **App not redeploying?**
  - Try making a small change to trigger a redeploy
  - Check the deployment logs in Streamlit Cloud

- **Need help?**
  - Check the Streamlit Cloud documentation
  - Review the error message in your app for specific details


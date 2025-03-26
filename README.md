# portfolio-that-talks ✨🗣️

## Hey there, future employers (and curious minds)! 👋

Welcome to **portfolio-that-talks**, the app that makes your portfolio... well, *talk*!  Think of it as giving your resume and GitHub projects a voice, powered by the magic of AI.  Instead of just listing your skills, let's have an AI peek at your awesome work and give you (and maybe even *you*!) some cool insights.

**Basically, this app is like:**

*   **Your Resume:**  "Hey AI, meet my resume! It's got all the good stuff."
*   **Your GitHub Projects:** "And check out these projects! They're where the *real* magic happens."
*   **Google's AI (Gemini Pro):** "Okay, okay, I see you.  Let me analyze this and tell you what's *really* going on here."
*   **You:** "🤯 Whoa!  My portfolio... *talks*! What does it say about me?"

This little app is your personal portfolio analyst in a box (well, in a Streamlit app!).  It's super easy to set up and lets you quickly get an AI-powered perspective on your skills and experience.  Let's make your portfolio do the talking!

## Get This Portfolio Chatting! 🗣️ Setup Instructions

Setting up **portfolio-that-talks** is easier than teaching a parrot to say "Hello world!" (and probably more useful for your career).  Here's the super-simple guide:

1.  **Grab the Goodies:**
    Make sure you've got Python on your machine (like, Python 3.8 or newer).  Then, let's use `uv` to snag the libraries we need. Open your terminal and type this in like you mean it:

    ```bash
    uv pip install -r pyproject.toml
    ```

2.  **Google's Secret Sauce (API Key Time!):**
    To make the AI magic happen, we need a key from Google.  Don't worry, it's not a *real* key, more like a secret password.

    *   Head over to [Google Cloud Console](https://console.cloud.google.com/) and create a project (if you haven't already). Think of it as your secret lab for AI experiments!
    *   Find and **enable the Vertex AI API** in your project's settings.  It's like turning on the AI power switch.
    *   Go to "Credentials" and create an **API Key**.  Copy this key – it's your magic word to talk to Google's AI.  Treat it like a precious gem!

3.  **Whisper the Secret Key to Streamlit:**
    Streamlit has a cool way to keep secrets safe (like your API key!).

    *   In the same folder as `portfolio_app.py`, make a new folder called `.streamlit`.  It's like your secret hideout for configurations.
    *   Inside `.streamlit`, create a file named `secrets.toml`.  Think of it as your secret diary.
    *   In `.env`, write this, but replace `YOUR_API_KEY` with the actual key you got from Google:

        ```toml
        GOOGLE_API_KEY = "YOUR_API_KEY"
        ```

4.  **Your Resume - In Plain Words:**
    We need your resume in a simple text file so the AI can read it easily.

    *   Create a file called `your_resume.txt` in the same folder as `portfolio_app.py`.
    *   Copy and paste the *text* of your resume into `your_resume.txt`.  Think of it as giving the AI a plain and simple version of your awesomeness.

5.  **Launch the Talking Portfolio! 🚀**
    Okay, we're ready to launch! Open your terminal, navigate to the folder, and type:

    ```bash
    streamlit run portfolio_app.py
    ```

## How It Works (The Fun & Easy Explanation)

**portfolio-that-talks** is built with a few cool pieces working together:

*   **Streamlit:** This is the magic wand that makes the app look nice and easy to use in your browser. It's like the friendly face of your talking portfolio.
*   **GitHub API:**  Think of this as a special messenger that goes to GitHub and says, "Hey GitHub, show me all the public projects for [your username]!"  It brings back a list of your awesome projects.
*   **AI (The Brains!):** This is the super-smart AI – a Large Language Model (LLM).  We feed it your resume and project descriptions and ask it to be your portfolio analyst.  It's like asking a really smart friend to review your work and give you feedback.
*   **Secrets (The Security Guard):**  Keeps your AI API key safe and sound, so only *you* can make your portfolio talk.

**Basically, the app:**

1.  Shows off your resume and GitHub projects in a cool way.
2.  Sends your resume and project info to the AI.
3.  The AI thinks hard and then spits out a summary of your skills and experience based on what it sees.
4.  You get to see what your portfolio is *saying* about you!

It's a fun and quick way to get an AI's perspective on your portfolio.  Go ahead, make your portfolio talk! 🎉
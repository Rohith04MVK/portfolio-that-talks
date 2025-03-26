import streamlit as st
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import fitz  # PyMuPDF
import re  # For basic text cleanup
from gtts import gTTS
from io import BytesIO

# --- Configuration ---
GITHUB_USERNAME = "Rohith04MVK"  # <--- REPLACE THIS
RESUME_FILE = "resume.pdf"
MODEL_NAME = "gemini-2.0-flash"  # Or "gemini-pro"
BOT_AVATAR = "🤖"
USER_AVATAR = "👤"
BOT_NAME = "Portfolio Assistant"

# --- Load API Key ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Helper Functions (Cached) ---

def get_github_repos(_username):
    """Fetches public repository data from GitHub."""
    repos_summary = []
    api_url = f"https://api.github.com/users/{_username}/repos?sort=updated&per_page=30"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        for repo in data:
            repos_summary.append(
                f"- {repo.get('name', 'N/A')}: {repo.get('description', 'No description')} (Lang: {repo.get('language', 'N/A')})"
            )
        logger.info(f"Fetched {len(repos_summary)} repos for {_username}")
        return "\n".join(repos_summary) if repos_summary else "No public repositories found or fetch failed."
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout fetching GitHub repos for {_username}")
        st.toast("⚠️ GitHub request timed out.", icon="⏳")
        return "Could not fetch GitHub repositories due to timeout."
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching GitHub repos for {_username}: {e}")
        st.toast(f"⚠️ Error fetching GitHub data: {e}", icon="❌")
        return "Could not fetch GitHub repositories."
    except Exception as e:
        logger.error(f"Unexpected error fetching GitHub repos: {e}")
        return "An unexpected error occurred while fetching GitHub data."

def load_resume_text(_filepath):
    """Loads and extracts text from a PDF resume."""
    full_text = ""
    if not os.path.exists(_filepath):
        logger.error(f"Resume PDF not found at {_filepath}")
        return None

    try:
        with fitz.open(_filepath) as doc:
            for page in doc:
                page_text = page.get_text("text", sort=True)
                if page_text:
                    full_text += page_text + "\n---\n"
        logger.info(f"Successfully extracted text from PDF: {_filepath}")
        full_text = re.sub(r'\n\s*\n', '\n\n', full_text)
        full_text = re.sub(r' +', ' ', full_text)
        full_text = full_text.strip()
        return full_text
    except Exception as e:
        logger.error(f"Error reading or processing PDF file {_filepath}: {e}")
        st.toast(f"⚠️ Error reading resume PDF: {e}", icon="❌")
        return "Error reading resume file."

# --- Google AI Function ---

def generate_llm_response(context, chat_history, user_query, api_key):
    """Generates text using the Google Generative AI API with chat history."""
    if not api_key:
        logger.error("Google API Key is missing.")
        st.error("AI Service Error: API key not configured.")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)

        history_for_prompt = []
        for msg in chat_history[-6:]:
            role = "user" if msg["role"] == "user" else "model"
            history_for_prompt.append(
                {"role": role, "parts": [msg["content"]]})
                
        system_prompt = f"""you are rohith (or a digital clone of him) an intelligent agent representing rohith, respond in first person not in third person, try to be less generic capture what its like to be rohith while being humble, built to analyze and describe the rohith's portfolio. My core function is to understand and process information such as resume content, projects, repositories, and other related details. I specialize in providing clear, concise, and insightful responses based on the user’s queries. I don’t just summarize—I analyze, offering my own thoughts and perspectives where relevant.

--- PROFILE CONTEXT ---
Resume:
{context['resume']}

Recent GitHub Projects:
{context['github']}
--- END CONTEXT ---
"""
        chat_session = model.start_chat(history=history_for_prompt)
        response = chat_session.send_message(
            f"{system_prompt}\n\nUser Question: {user_query}")

        logger.info("Successfully generated response from LLM.")
        if response.parts:
            return response.text
        else:
            logger.warning(
                f"LLM response empty/blocked. Reason: {response.prompt_feedback.block_reason}")
            st.toast(
                f"AI response issue: {response.prompt_feedback.block_reason}", icon="⚠️")
            return f"I couldn't generate a response for that. Reason: {response.prompt_feedback.block_reason}"
    except Exception as e:
        logger.error(f"Error calling Google Generative AI API: {e}")
        if "API key not valid" in str(e):
            st.error("AI Service Error: Invalid Google API Key.")
            return "AI service error: Invalid API Key."
        else:
            st.error(f"AI Service Error: {e}")
            return f"Sorry, I encountered an error: {e}"

# Page Config
st.set_page_config(
    page_title=f"{GITHUB_USERNAME}'s Portfolio AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown(
"""
<style>
/* General Page Styling /
.stApp {
background: linear-gradient(to bottom right, #000, #000); / Lighter background /
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; / More readable font */
}


/* Header Styling */
.stApp > header {
background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white header */
backdrop-filter: blur(5px); /* Optional blur for the header */
padding: 0.5rem 0;
}

/* Main Container */
.main .block-container {
max-width: 800px; /* Slightly wider for better flow */
margin: auto;
padding: 2rem; /* Increased padding */
}

/* Chat Message Styling */
.stChatMessage {
background-color: #000; /* Light background for bot messages */
border-radius: 12px; /* Softer rounded corners */
padding: 14px 18px; /* Slightly more padding */
margin-bottom: 12px;
box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05); /* Softer shadow */
font-size: 1rem;
line-height: 1.5; /* Improved line height for readability */
color: #fff; /* Darker text for better contrast on light background */
}

/* User Message Styling */
div.stChatMessage:nth-child(even) { /* Target even-numbered chat messages (assuming user messages alternate) */
background-color: #000; /* Slightly different for user messages */
}

/* Chat Input Box */
.stChatInput {
background-color: #000; /* White input background */
border-radius: 12px;
padding: 12px 16px;
box-shadow: 0px -1px 3px rgba(0, 0, 0, 0.05); /* Softer shadow */
margin-top: 1rem; /* Add some space above the input */
}

.stChatInput textarea {
background-color: transparent;
border: none;
font-size: 1rem;
color: #000; /* Darker text in the input */
}

/* Title Styling */
h1 {
text-align: center;
color: #000; /* Darker title color */
font-size: 2rem; /* Slightly larger title */
font-weight: 500; /* Medium font weight */
margin-bottom: 1.5rem;
}

/* Welcome Message */
.welcome-message {
text-align: center;
color: #000; /* Muted welcome message color */
font-size: 1.1rem;
margin-bottom: 2.5rem;
}
</style>

""",
unsafe_allow_html=True,
)

# --- Initial Checks ---
if not GITHUB_USERNAME or GITHUB_USERNAME == "YOUR_GITHUB_USERNAME":
    st.error("🛑 Configuration Error: Please set your `GITHUB_USERNAME` in the script.")
    st.stop()

if not GOOGLE_API_KEY:
    st.error("🛑 Configuration Error: `GOOGLE_API_KEY` not found. Please set it in your `.env` file.")
    st.stop()

# --- Load Profile Data ---
if 'profile_context' not in st.session_state:
    logger.info("Loading profile context for the first time...")
    resume_text = load_resume_text(RESUME_FILE)
    github_summary = get_github_repos(GITHUB_USERNAME)

    if resume_text is None:
        st.error(f"Fatal Error: Resume file '{RESUME_FILE}' not found. Cannot proceed.")
        st.stop()
    elif "Error reading" in resume_text:
        st.warning(f"Warning: There was an issue reading the resume PDF: {resume_text}")

    st.session_state.profile_context = {
        "resume": resume_text if resume_text and "Error" not in resume_text else "Resume data unavailable or unreadable.",
        "github": github_summary if github_summary else "GitHub data unavailable."
    }
    logger.info("Profile context loaded into session state.")
    st.toast("Profile data loaded!", icon="📄")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_greeting = f"Hi there! I'm Rohith! ask me anything!"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})
    logger.info("Chat history initialized.")

# --- App Title and Welcome ---
st.title(f"Chat with {GITHUB_USERNAME}'s AI Assistant")
st.markdown(f"<div class='welcome-message'>Ask questions about {GITHUB_USERNAME}'s skills, experience, or projects!</div>", unsafe_allow_html=True)

# --- Display Chat Messages ---
for message in st.session_state.messages:
    avatar = BOT_AVATAR if message["role"] == "assistant" else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input(f"Ask about {GITHUB_USERNAME}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
            response = generate_llm_response(
                context=st.session_state.profile_context,
                chat_history=st.session_state.messages,
                user_query=prompt,
                api_key=GOOGLE_API_KEY
            )
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # --- Text-to-Speech ---
                try:
                    tts = gTTS(response, lang='en', )
                    sound_file = BytesIO()
                    tts.write_to_fp(sound_file)
                    sound_file.seek(0)
                    st.audio(sound_file, format="audio/mp3")
                except Exception as tts_error:
                    logger.error(f"TTS generation error: {tts_error}")
                    st.toast("⚠️ Could not generate audio for the response.", icon="❌")
            else:
                fallback_message = "Sorry, I couldn't process that request."
                st.markdown(fallback_message)
                st.session_state.messages.append({"role": "assistant", "content": fallback_message})

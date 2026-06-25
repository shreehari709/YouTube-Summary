# YouTube-Summary

Here is a complete, professional, and highly detailed `README.md` tailored specifically for your project. It covers everything from local setup to your advanced Render deployment and the cookie workaround.

You can copy this entirely and save it as `README.md` in your main project folder.

---

```markdown
# 📝 AI YouTube Notes Generator

A lightning-fast, full-stack web application that takes any YouTube video link, extracts the transcript (bypassing cloud IP blocks), and uses Google's Gemini 2.5 Flash AI to generate highly structured, zero-fluff study notes. 

Built for students and developers who want to extract the core value of long lectures and tutorials instantly.

## ✨ Features
* **Universal Link Parsing:** Accepts standard YouTube links, Mobile (`youtu.be`), and Shorts.
* **Smart AI Summarization:** Instructed specifically to ignore fluff, intro-filler, and repetitive sentences, outputting dense, high-impact bullet points.
* **Beautiful Markdown Rendering:** Transforms raw AI markdown into a clean, readable UI using Marked.js and Tailwind CSS.
* **One-Click Export:** Download your generated notes directly as a Microsoft Word (`.doc`) file.
* **Anti-Bot Bypass:** Custom HTTP session handling utilizing `cookies.txt` to bypass YouTube's aggressive data-center IP blocks on cloud providers like Render.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Model:** Google Gemini 2.5 Flash (`google-genai`)
* **Transcript Extraction:** `youtube-transcript-api`
* **Frontend:** Vanilla HTML/JS, Tailwind CSS (via CDN), Marked.js (via CDN)
* **Deployment:** Render

---

## 📁 Project Structure
Ensure your repository matches this exact structure before deploying:
```text
YouTubeAI/
├── app.py                  # FastAPI backend logic and routing
├── index.html              # Frontend UI and API calls
├── requirements.txt        # Python dependencies
├── .gitignore              # Secures environment variables and pycache
└── README.md               # Project documentation

```

---

## 💻 Local Setup Instructions

Follow these steps to run the application on your own computer.

### 1. Prerequisites

* Python 3.8+ installed on your machine.
* A free [Google Gemini API Key](https://aistudio.google.com/).

### 2. Clone and Install

Open your terminal and run the following commands:

```bash
# Clone the repository (replace with your repo link)
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

```

### 3. Environment Variables

Create a file named exactly `.env` in the root folder and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here

```

*(Note: Do not upload this file to GitHub! The `.gitignore` file will prevent this automatically).*

### 4. Run the Server

Start the local Uvicorn server:

```bash
uvicorn app:app --reload

```

Open your web browser and navigate to `http://127.0.0.1:8000/`.

---

## 🚀 Deployment (Render) & The YouTube IP Block

Deploying this app to a cloud provider like Render triggers YouTube's anti-bot protection because cloud server IP addresses are heavily restricted. This project bypasses the block by injecting an authenticated YouTube session cookie into the API request.

### Step 1: Get your `cookies.txt`

1. Open Google Chrome and log into a **secondary/dummy Google account** (Do NOT use your main account, as automated scrapers risk being banned).
2. Install the **"Get cookies.txt LOCALLY"** Chrome extension.
3. Go to YouTube, click the extension, and export your cookies as a `.txt` file.

### Step 2: Deploy to Render

1. Push this repository to GitHub.
2. In Render, create a new **Web Service** linked to your repo.
3. Set the **Build Command**: `pip install -r requirements.txt`
4. Set the **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. In the **Environment Variables** section, add your `GEMINI_API_KEY`.

### Step 3: Inject the Cookies

1. In your Render Dashboard, go to your Web Service -> **Environment** -> **Secret Files**.
2. Click **Add Secret File**.
3. Name it exactly `cookies.txt`.
4. Paste the entire contents of the cookie file you downloaded in Step 1.
5. Save and trigger a manual deploy.

The `app.py` script is designed to hunt for this file inside Render's secure `/etc/secrets/` directory and use it to authenticate the transcript request, bypassing the IP block!

---

## 💡 How It Works (Under the Hood)

1. **Frontend Interaction:** The user pastes a URL into `index.html`. JavaScript intercepts this, shows a loading state, and sends a `POST` request to the backend.
2. **Regex Parsing:** Python (`app.py`) uses Regular Expressions to cleanly slice the 11-character Video ID from any messy YouTube URL format.
3. **Session Spoofing:** A custom `requests.Session()` is built using the `cookies.txt` file to trick YouTube into thinking the cloud server is a standard human web browser.
4. **AI Processing:** The raw transcript text is sent to Gemini alongside strict system instructions to parse the text into structured Markdown.
5. **UI Rendering:** The backend returns the string to the frontend, where `marked.js` instantly converts the Markdown tags into beautifully styled HTML headers and bullet points.

---

*Built with Python, FastAPI, and Gemini AI.*

```

```

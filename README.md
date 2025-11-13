# multi_-agent-AI-system
Multi-agent AI system as a personalized study system
 AI Study Co-Pilot

The AI Study Co-Pilot is a sophisticated, localized, and persistent study assistant built with Streamlit. It uses Offline Large Language Models (LLMs) via Ollama to analyze user-uploaded PDF notes and instantly generate study materials like summaries, flashcards, and quizzes. All generated study sets are saved securely using Firebase Firestore for persistent access.

This application features a clean, conversational UI design (inspired by modern chat interfaces) and supports English and Hindi localization.

Features

PDF Analysis: Upload any PDF document to extract and analyze the contents.

Offline LLM Integration: Utilizes Ollama to run models like llama3 locally, ensuring fast, private, and free AI generation without external API keys (after initial setup).

Generated Study Materials:

Summary: A concise overview of the document's core concepts.

Flashcards: Interactive Q&A pairs for memorization, complete with Text-to-Speech (TTS) audio.

Quizzes: Multiple-choice questions to test understanding.

Doubt Solver: Ask specific questions about the document content.

Revision Planner: Generates a suggested study schedule based on days and difficulty.

Data Persistence (Library): Save and load entire study sets (flashcards, quizzes, summary) using Firebase Firestore persistence.


Clean UI: Modern, responsive, single-column design inspired by chat interfaces for focused studying.

 Prerequisites

Before running the application, you need to set up two main components:

1. Ollama (Offline LLM Server)

This application requires an active Ollama instance running on your machine to power the AI generation agents.

Install Ollama: Download and install the application from https://ollama.com/.

Run Ollama: Ensure the Ollama server is running in the background.

Pull the Model: Open your terminal and pull the recommended model (llama3:8b is highly suggested for performance and quality):

ollama pull llama3


(Note: If you use a different model, you must update the model name within the ai_agents.py file.)

2. Firebase Firestore (Database Persistence)

Study sets are stored in the cloud using Firebase for user authentication and data persistence.

Create a Firebase Project: Go to the Firebase Console and create a new project.

Set up Firestore: Enable Firestore Database in Native mode.

Get Configuration: In your Project Settings, find the Web App configuration snippet. This looks like:

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_ID",
  appId: "YOUR_APP_ID"
};


 Installation and Setup

1. Clone the Repository

git clone [https://github.com/your-username/ai-study-copilot.git](https://github.com/your-username/ai-study-copilot.git)
cd ai-study-copilot


2. Create Python Environment

It is highly recommended to use a virtual environment:

python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
.\venv\Scripts\activate    # On Windows


3. Install Dependencies

Install all required Python packages:

pip install -r requirements.txt


(You will need to create the requirements.txt file listing all used packages: streamlit, ollama, pypdf, gTTS, firebase-admin, etc.)

⚙️ How to Run the Application

1. Set Environment Variables

Since the application relies on the Firebase configuration being available in the environment, you must set the following variables in your terminal or a .env file before running Streamlit:

Variable

Value

Description

FIREBASE_CONFIG_JSON

{"apiKey": "...", "projectId": "...", ...}

Entire Firebase Config as a JSON string.

OLLAMA_HOST

http://localhost:11434

Your Ollama server address.

Example (Linux/macOS):

export FIREBASE_CONFIG_JSON='{"apiKey": "YOUR_API_KEY", "authDomain": "...", "projectId": "...", "appId": "..."}'
export OLLAMA_HOST="http://localhost:11434"


2. Start Streamlit

Run the application using the Streamlit command:

streamlit run app.py


The application will open in your default web browser.

 File Structure

The project is modularized into several Python files for clarity:

File

Description

app.py

The main Streamlit application file. Manages the UI, state, routing, and user interaction logic.

localization.py

Stores all UI text for English and Hindi, handling localization dynamically.

reader.py

Handles PDF file processing, reading content, and cleaning the extracted text.

ai_agents.py

Contains the core functions for interacting with Ollama to generate summaries, quizzes, flashcards, etc.

planner.py

Logic for generating the structured study revision plan.

firestore_db.py

Manages all read/write operations with the Firebase Firestore database (saving and loading study sets).

AI Co-Pilot/
├── __pycache__/
│   ├── ai_agents.cpython-313.pyc
│   ├── firestore_db.cpython-313.pyc
│   ├── localization.cpython-313.pyc
│   ├── planner.cpython-313.pyc
│   └── reader.cpython-313.pyc
├── .venv/
│   ├── etc/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── share/
├── .gitignore
├── ServiceAccountKey.json
├── ai_agents.py
├── app.py
├── firestore_db.py
├── localization.py
├── planner.py
├── reader.py
└── study_library.db

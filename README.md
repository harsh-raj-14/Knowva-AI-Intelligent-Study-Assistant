# AI StudyMate — Modern UI Edition

A Streamlit-based AI learning assistant that turns PDF notes or pasted text into summaries, important questions, MCQ quizzes, flashcards, simple explanations, and study plans. Includes question answering over uploaded PDF text.

## Features
- Modern responsive blue/purple interface with sidebar navigation and feature cards
- PDF text extraction
- AI study material generation with Gemini
- Ask questions about the PDF using keyword-overlap chunk retrieval
- Download generated output as a `.txt` file
- Clear errors for common API setup issues

## Important limitation
The included question-answering retrieval uses **keyword overlap**, not embedding-based semantic search or a vector database. Scanned/image-only PDFs need OCR before upload. Treat AI outputs as study aids and verify important information.

## Setup on Windows / VS Code
1. Extract the ZIP and open the project folder in VS Code.
2. Open the terminal and create a virtual environment:
   ```powershell
   python -m venv venv
   .\\venv\\Scripts\\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`.
5. Add your own Gemini API key to `.env`:
   ```env
   GEMINI_API_KEY=your_private_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```
6. Start the app:
   ```powershell
   streamlit run app.py
   ```

## Security
- Never commit or share `.env`.
- If an API key has been shared publicly or in a chat, revoke it and create a replacement.
- Model availability, usage limits, and billing depend on your Gemini account.

## Project structure
```text
AI-StudyMate-Modern/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── studymate/
    ├── __init__.py
    ├── documents.py
    ├── prompts.py
    └── rag.py
```

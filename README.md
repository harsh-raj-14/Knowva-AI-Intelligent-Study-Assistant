# Knowva AI — Intelligent Study Assistant

**Your Notes. Reimagined by AI.**

Knowva AI is a Generative AI-powered learning assistant that transforms study materials into structured summaries, important questions, MCQ quizzes, flashcards, and context-aware answers. It helps students understand complex concepts, revise efficiently, and prepare for exams using their own study documents.

## ✨ Features

- **PDF Document Processing:** Upload PDF study notes and extract their text.
- **AI-Powered Summarization:** Convert lengthy study material into concise, structured notes.
- **Important Question Generation:** Generate exam-oriented questions with answers.
- **MCQ Quiz Generator:** Create multiple-choice questions for self-assessment.
- **Flashcard Generation:** Turn key concepts and definitions into question-and-answer cards.
- **Ask Your PDF:** Ask questions about uploaded documents and receive answers based on retrieved content.
- **Simple Explanations:** Understand complex topics through beginner-friendly explanations.
- **Personalized Study Plans:** Generate structured revision plans from learning material.
- **Downloadable Results:** Export generated study content as text files.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Google Gemini API | Generative AI and question answering |
| PyPDF | PDF text extraction |
| python-dotenv | Environment variable management |

## 🏗️ Project Structure

```text
Knowva-AI/
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

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Knowva-AI.git
cd Knowva-AI
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Use a Gemini model available to your account. Never commit your `.env` file or expose your API key publicly.

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically `http://localhost:8501`.

## 🚀 How to Use

1. Launch Knowva AI.
2. Upload a PDF containing your study notes, or paste text into the study tools.
3. Select the feature you want to use.
4. Generate summaries, questions, quizzes, flashcards, explanations, or a study plan.
5. Use **Ask Your PDF** to ask questions about the uploaded material.
6. Download generated content for later revision.

## 🔎 Document Question Answering

Knowva AI divides extracted PDF text into overlapping chunks and retrieves relevant sections using keyword overlap. The selected context is passed to the Gemini API to generate a response.

**Current limitation:** Retrieval is keyword-based rather than embedding-based semantic search. Scanned PDFs without selectable text may require OCR before processing.

## 🔐 Security and Responsible Use

- Keep API keys in environment variables.
- Never commit `.env` or credentials to version control.
- Follow the Gemini API's applicable usage limits and terms.
- Verify AI-generated answers before relying on them for examinations or important decisions.
- Avoid uploading confidential documents or sensitive personal information.

## 🔮 Future Enhancements

- Embedding-based semantic search and vector database integration.
- Chat history and persistent user sessions.
- Interactive quizzes with scoring and progress tracking.
- Citation and page-reference support for PDF answers.
- OCR support for scanned documents.
- User authentication and personalized learning dashboards.
- Deployment with Streamlit Community Cloud.

## 🎯 Project Objective

The goal of Knowva AI is to make learning more interactive and efficient by combining document processing, Generative AI, and retrieval-based question answering in a unified study platform.

## 👨‍💻 Author

**Harsh Raj**  
B.Tech — Computer Science and Engineering

## 📄 License

This project is intended for educational and portfolio purposes. Add a license file if you plan to distribute or reuse the project publicly.

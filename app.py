import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from studymate.documents import extract_pdf_text
from studymate.rag import split_text, retrieve_relevant_chunks
from studymate.prompts import build_prompt

load_dotenv()
st.set_page_config(page_title="AI StudyMate", page_icon="📘", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#172554;--muted:#64748b;--blue:#4f46e5}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#f7f9ff;color:var(--ink)}
.block-container{padding-top:1.5rem;padding-bottom:3rem;max-width:1240px}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e8ecf5}
.brand{display:flex;align-items:center;gap:12px;margin:2px 0 25px}
.brand-icon{width:46px;height:46px;border-radius:15px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#4f46e5,#818cf8);color:white;font-size:25px;box-shadow:0 8px 20px #4f46e533}
.brand-name{font-family:Manrope,sans-serif;font-weight:800;font-size:20px;line-height:1.1;color:#172554}
.brand-sub{font-size:10px;color:#7c89a4;margin-top:5px;letter-spacing:1px}
.hero{background:linear-gradient(120deg,#eef2ff 0%,#f7f8ff 55%,#ecfeff 100%);border:1px solid #e0e7ff;border-radius:27px;padding:34px 36px;margin-bottom:24px}
.kicker{display:inline-block;padding:7px 12px;border-radius:999px;background:#ffffffc9;border:1px solid #dbe4ff;color:#4f46e5;font-weight:700;font-size:12px;margin-bottom:14px}
.hero h1{font-family:Manrope,sans-serif;font-size:clamp(30px,4vw,46px);line-height:1.12;letter-spacing:-1.5px;color:#172554;margin:0 0 12px;font-weight:800}
.hero h1 span{color:#4f46e5}
.hero p{color:#5b6682;font-size:15px;line-height:1.7;max-width:690px;margin:0}
.hero-foot{margin-top:20px;color:#66728b;font-size:12px}
.section-title{font-family:Manrope,sans-serif;font-size:22px;font-weight:800;color:#172554;margin:7px 0 5px}
.section-sub{font-size:13px;color:#71809b;margin-bottom:17px}
.feature{background:#fff;border:1px solid #e7eaf3;border-radius:18px;padding:18px;height:100%;box-shadow:0 5px 18px #17255406}
.feature-icon{width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:21px;margin-bottom:13px}
.feature h3{font-family:Manrope,sans-serif;font-size:15px;margin:0 0 7px;color:#172554}
.feature p{font-size:12px;line-height:1.55;color:#75819a;margin:0}
div[data-testid="stFileUploader"]{background:#fff;border:1px dashed #a5b4fc;border-radius:17px;padding:12px}
.stButton>button,.stDownloadButton>button{border-radius:12px;font-weight:700;min-height:42px;border:1px solid #e0e7ff}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#4f46e5,#6366f1);color:white;border:0}
.stButton>button:hover{border-color:#818cf8;transform:translateY(-1px)}
[data-testid="stMetric"]{background:#fff;border:1px solid #e7eaf3;border-radius:15px;padding:14px}
[data-testid="stTabs"] button{font-weight:700}
[data-testid="stForm"]{background:#fff;border:1px solid #e7eaf3;border-radius:18px;padding:18px}
.output{background:#fff;border:1px solid #e7eaf3;border-radius:18px;padding:20px}
.footer{text-align:center;color:#9aa4b8;font-size:11px;padding:30px 0 4px}
@media(max-width:700px){.hero{padding:24px 20px}.hero h1{font-size:31px}}
</style>
""", unsafe_allow_html=True)

def brand():
    st.markdown("""<div class="brand"><div class="brand-icon">✦</div><div>
    <div class="brand-name">AI StudyMate</div><div class="brand-sub">YOUR PERSONAL AI LEARNING SPACE</div>
    </div></div>""", unsafe_allow_html=True)

def gemini(prompt, system="You are AI StudyMate, a helpful and accurate learning assistant. Explain concepts clearly for students."):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Gemini API key not found. Add GEMINI_API_KEY to your .env file.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"system_instruction": system, "temperature": 0.4}
    )
    return response.text or "No text was returned. Please try again."

def make_prompt(task, text, extra=""):
    return build_prompt(task, text, extra)

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""
if "doc_name" not in st.session_state:
    st.session_state.doc_name = ""
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    brand()
    st.markdown("### Workspace")
    page = st.radio("Navigate", ["Overview", "Study tools", "Ask your PDF"], label_visibility="collapsed")
    st.divider()
    st.markdown("### Your document")
    if st.session_state.doc_text:
        st.success("PDF ready")
        st.caption(st.session_state.doc_name)
        st.caption(f"{len(st.session_state.doc_text):,} characters extracted")
        if st.button("Remove document", use_container_width=True):
            st.session_state.doc_text = ""
            st.session_state.doc_name = ""
            st.rerun()
    else:
        st.caption("Upload a PDF to unlock document-based study tools.")
    st.divider()
    st.markdown("<div style='font-size:12px;color:#8792a8'>Built with Streamlit + Gemini<br>Keep your API key private.</div>", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="kicker">✦ YOUR AI-POWERED STUDY PARTNER</div>
  <h1>Turn your notes into<br><span>smarter learning.</span></h1>
  <p>Upload a PDF and let AI StudyMate transform long study material into clear summaries, practice questions, flashcards, and answers grounded in your notes.</p>
  <div class="hero-foot">📄 PDF notes &nbsp; · &nbsp; ✨ AI summaries &nbsp; · &nbsp; 🧠 Active recall &nbsp; · &nbsp; 💬 Ask questions</div>
</div>
""", unsafe_allow_html=True)

if page == "Overview":
    st.markdown('<div class="section-title">Everything you need to study smarter</div><div class="section-sub">A simple workspace for turning reading into understanding.</div>', unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    features = [
        ("📄", "#eef2ff", "PDF to notes", "Upload class notes or textbooks in PDF format."),
        ("✨", "#ecfdf5", "AI summaries", "Turn long material into clear, structured notes."),
        ("🧩", "#fff7ed", "Practice questions", "Generate exam-style questions and MCQs."),
        ("🗂️", "#f5f3ff", "Flashcards", "Review key terms with quick question-and-answer cards.")
    ]
    for c, (ico, bg, title, desc) in zip(cols, features):
        with c:
            st.markdown(f'<div class="feature"><div class="feature-icon" style="background:{bg}">{ico}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Start with your study material</div><div class="section-sub">Upload a PDF below. Text-based PDFs work best.</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a PDF", type=["pdf"], key="overview_pdf", help="Maximum recommended size: 15 MB.")
    if uploaded:
        with st.spinner("Reading your PDF..."):
            try:
                extracted = extract_pdf_text(uploaded)
                if not extracted.strip():
                    st.warning("No selectable text was found. If this is a scanned PDF, run OCR first.")
                else:
                    st.session_state.doc_text = extracted
                    st.session_state.doc_name = uploaded.name
                    st.success(f"Ready! Extracted {len(extracted):,} characters from {uploaded.name}.")
                    st.info("Open **Study tools** or **Ask your PDF** in the sidebar.")
            except Exception as e:
                st.error(f"Could not read this PDF: {e}")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your workflow</div>', unsafe_allow_html=True)
    step_cols = st.columns(3)
    for c, n, title, desc in [
        (step_cols[0], "01", "Upload", "Add a PDF with your notes."),
        (step_cols[1], "02", "Generate", "Choose a study tool and customize it."),
        (step_cols[2], "03", "Review", "Read, copy, and revise the results.")
    ]:
        with c:
            st.markdown(f'<div class="feature"><div style="font-size:12px;font-weight:800;color:#6366f1;margin-bottom:8px">STEP {n}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif page == "Study tools":
    st.markdown('<div class="section-title">Study tools</div><div class="section-sub">Generate useful learning material from your PDF or pasted notes.</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload or replace your PDF", type=["pdf"], key="tools_pdf")
    if uploaded:
        try:
            extracted = extract_pdf_text(uploaded)
            if extracted.strip():
                st.session_state.doc_text = extracted
                st.session_state.doc_name = uploaded.name
                st.success(f"Loaded {uploaded.name}")
        except Exception as e:
            st.error(str(e))
    source_mode = st.radio("Content source", ["Uploaded PDF", "Paste notes"], horizontal=True)
    if source_mode == "Paste notes":
        source_text = st.text_area("Paste your study material", height=180, placeholder="Paste class notes, textbook excerpts, or a topic outline...")
    else:
        source_text = st.session_state.doc_text
        if source_text:
            st.caption(f"Using: {st.session_state.doc_name}")
            with st.expander("Preview extracted text"):
                st.text(source_text[:5000] + ("..." if len(source_text) > 5000 else ""))
        else:
            st.info("Upload a PDF on this page or from Overview, or choose Paste notes.")
    st.divider()
    task = st.selectbox("What would you like to create?", ["Summary", "Important questions", "MCQ quiz", "Flashcards", "Explain simply", "Study plan"])
    level = st.select_slider("Difficulty", options=["Beginner", "Intermediate", "Exam revision"], value="Beginner")
    count = st.slider("Number of items (where applicable)", min_value=5, max_value=20, value=10, step=5)
    if st.button("✨ Generate study material", type="primary", use_container_width=True):
        if not source_text or len(source_text.strip()) < 40:
            st.warning("Please upload a readable PDF or paste at least a few sentences of notes.")
        else:
            extra = f"Difficulty: {level}. Generate approximately {count} items when applicable. Use headings and readable formatting."
            with st.spinner("Creating your study material..."):
                try:
                    result = gemini(make_prompt(task, source_text[:45000], extra))
                    st.session_state.history.append({"task": task, "result": result})
                    st.session_state.last_result = result
                    st.session_state.last_task = task
                except Exception as e:
                    st.error("Generation failed. Check your API key, model name, internet connection, and Gemini quota.")
                    with st.expander("Technical details"):
                        st.code(str(e))
    if st.session_state.get("last_result"):
        st.markdown(f'<div class="section-title">Your {st.session_state.get("last_task","study")} is ready</div>', unsafe_allow_html=True)
        st.markdown('<div class="output">', unsafe_allow_html=True)
        st.markdown(st.session_state.last_result)
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download result as text", data=st.session_state.last_result, file_name="ai_studymate_result.txt", mime="text/plain")

else:
    st.markdown('<div class="section-title">Ask your PDF</div><div class="section-sub">Ask questions about your uploaded material. Answers are based on the most relevant matching text chunks.</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload or replace your PDF", type=["pdf"], key="qa_pdf")
    if uploaded:
        try:
            extracted = extract_pdf_text(uploaded)
            if extracted.strip():
                st.session_state.doc_text = extracted
                st.session_state.doc_name = uploaded.name
                st.success(f"Loaded {uploaded.name}")
        except Exception as e:
            st.error(str(e))
    if not st.session_state.doc_text:
        st.info("Upload a PDF on this page or from Overview to start asking questions.")
    else:
        st.markdown(f"**Current document:** {st.session_state.doc_name}")
        question = st.text_area("Your question", placeholder="Example: Explain the difference between precision and recall.", height=90)
        if st.button("Ask StudyMate", type="primary", use_container_width=True):
            if not question.strip():
                st.warning("Enter a question first.")
            else:
                chunks = split_text(st.session_state.doc_text)
                relevant = retrieve_relevant_chunks(question, chunks, top_k=4)
                context = "\n\n---\n\n".join(relevant)
                prompt = f"Answer the student's question using the context below. If the context does not contain the answer, say so clearly. Do not invent citations. Keep the answer helpful and concise.\n\nCONTEXT:\n{context}\n\nQUESTION: {question}"
                with st.spinner("Finding an answer in your notes..."):
                    try:
                        answer = gemini(prompt)
                        st.markdown('<div class="output">', unsafe_allow_html=True)
                        st.markdown("### Answer")
                        st.markdown(answer)
                        st.markdown('</div>', unsafe_allow_html=True)
                        with st.expander("View retrieved context"):
                            st.write(context)
                    except Exception as e:
                        st.error("Could not generate an answer. Check your API key, model name, internet connection, and quota.")
                        with st.expander("Technical details"):
                            st.code(str(e))

st.markdown('<div class="footer">AI StudyMate · Learn with clarity, revise with confidence.</div>', unsafe_allow_html=True)

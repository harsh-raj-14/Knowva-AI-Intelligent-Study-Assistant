import re
from collections import Counter

def split_text(text, chunk_size=1100, overlap=180):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def _tokens(text):
    return re.findall(r"[a-zA-Z0-9]{2,}", text.lower())

def retrieve_relevant_chunks(query, chunks, top_k=4):
    q = Counter(_tokens(query))
    if not q or not chunks:
        return chunks[:top_k]
    scored = []
    for i, chunk in enumerate(chunks):
        c = Counter(_tokens(chunk))
        score = sum(min(q[t], c[t]) for t in q)
        scored.append((score, i, chunk))
    scored.sort(key=lambda x: (x[0], -x[1]), reverse=True)
    selected = [x[2] for x in scored[:top_k] if x[0] > 0]
    return selected or chunks[:min(top_k, len(chunks))]

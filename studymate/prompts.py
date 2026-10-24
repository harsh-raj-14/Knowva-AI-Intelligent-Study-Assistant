def build_prompt(task, source_text, extra=""):
    task_instructions = {
        "Summary": "Create a clear, structured summary with headings, key ideas, definitions, and a short recap.",
        "Important questions": "Create exam-relevant questions from the source. Include a mix of short-answer and longer conceptual questions. Provide concise model answers.",
        "MCQ quiz": "Create multiple-choice questions with four options each. Mark the correct answer and explain why it is correct.",
        "Flashcards": "Create question-and-answer flashcards. Keep each answer short and useful for active recall.",
        "Explain simply": "Explain the source in beginner-friendly language with simple examples and define technical terms.",
        "Study plan": "Create a practical study plan based only on the source. Break it into focused sessions and include revision and self-testing."
    }
    instruction = task_instructions.get(task, "Help the student learn the source material.")
    return f"""Task: {task}
Instructions: {instruction}
{extra}

Use the source material as the primary reference. Do not claim facts that are not supported by it; if adding general context, label it clearly. Format the response in Markdown.

SOURCE MATERIAL:
{source_text}
"""

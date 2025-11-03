import pandas as pd
import random
import spacy
from spacy.pipeline import EntityRuler
import customtkinter as ctk
from tkinter import scrolledtext, END

# ==================== Setup ====================

# Set appearance
ctk.set_appearance_mode("dark")  # dark mode
ctk.set_default_color_theme("blue")  # nice blue accent

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ---------- Safe EntityRuler setup (fixed for spaCy v3+) ----------
patterns = [
    {"label": "TECH_COMPANY", "pattern": "Microsoft"},
    {"label": "TECH_COMPANY", "pattern": "Google"},
    {"label": "TECH_COMPANY", "pattern": "Apple"},
    {"label": "TECH_COMPANY", "pattern": "OpenAI"},
    {"label": "UNIVERSITY", "pattern": "Cairo University"},
    {"label": "COUNTRY", "pattern": "Egypt"},
]

if "entity_ruler" not in nlp.pipe_names:
    try:
        nlp.add_pipe("entity_ruler", before="ner")
    except ValueError:
        nlp.add_pipe("entity_ruler")

ruler = nlp.get_pipe("entity_ruler")
ruler.add_patterns(patterns)


# ==================== Load CoNLL Dataset ====================

def load_conll(file_path):
    """Reads a CoNLL-format file and returns a list of sentences."""
    sentences = []
    with open(file_path, "r", encoding="utf-8") as f:
        words = []
        for line in f:
            if line.strip() == "":
                if words:
                    sentences.append(" ".join(words))
                    words = []
            else:
                parts = line.split()
                if len(parts) >= 1:
                    words.append(parts[0])
        if words:
            sentences.append(" ".join(words))
    return sentences

# Load all 3 files (adjust paths if needed)
train_sentences = load_conll("eng.train")
testa_sentences = load_conll("eng.testa")
testb_sentences = load_conll("eng.testb")

# Combine all
all_sentences = train_sentences + testa_sentences + testb_sentences

# ==================== GUI Setup ====================

root = ctk.CTk()
root.title("Named Entity Recognition (NER) - CoNLL2003")
root.geometry("900x700")

# Configure grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Title Label
title_label = ctk.CTkLabel(
    root,
    text="🧠 Named Entity Recognition (NER)",
    font=("Arial", 24, "bold"),
    text_color="#00BFFF",
)
title_label.grid(row=0, column=0, pady=20)

# Text box for input
input_box = scrolledtext.ScrolledText(
    root,
    wrap="word",
    width=100,
    height=8,
    font=("Consolas", 14),
    bg="#1E1E1E",
    fg="#FFFFFF",
    insertbackground="#00BFFF",
    relief="flat",
    borderwidth=2,
)
input_box.grid(row=1, column=0, padx=30, sticky="nsew")

def analyze_text():
    text = input_box.get("1.0", END).strip()
    if not text:
        result_box.configure(state="normal")
        result_box.delete("1.0", END)
        result_box.insert("1.0", "⚠️ Please enter or load some text first.")
        result_box.configure(state="disabled")
        return

    mode = ner_mode.get()
    result_box.configure(state="normal")
    result_box.delete("1.0", END)

    if mode == "Rule-based":
        # Create a blank pipeline with only the entity ruler
        from spacy.lang.en import English
        nlp_rule = English()
        ruler = nlp_rule.add_pipe("entity_ruler")
        ruler.add_patterns(patterns)
        doc = nlp_rule(text)

    elif mode == "Model-based":
        # Use the pretrained spaCy model only
        nlp_model = spacy.load("en_core_web_sm")
        doc = nlp_model(text)

    else:  # Combined
        doc = nlp(text)

    # Display entities
    if doc.ents:
        for ent in doc.ents:
            result_box.insert(END, f"{ent.text:<25} →  {ent.label_}\n")
    else:
        result_box.insert(END, "No named entities found.")
    result_box.configure(state="disabled")


# Function to load a random CoNLL sentence
def load_random_sentence():
    sentence = random.choice(all_sentences)
    input_box.delete("1.0", END)
    input_box.insert("1.0", sentence)

# --- NER mode selection (model-based, rule-based, or both) ---
mode_label = ctk.CTkLabel(
    root,
    text="Select NER Mode:",
    font=("Arial", 16, "bold"),
    text_color="#00BFFF",
)
mode_label.grid(row=4, column=0, sticky="w", padx=40, pady=(10, 0))

ner_mode = ctk.CTkComboBox(
    root,
    values=["Model-based", "Rule-based", "Combined"],
    font=("Arial", 14),
    width=250,
)
ner_mode.set("Combined")
ner_mode.grid(row=5, column=0, sticky="w", padx=40, pady=(0, 10))


# Buttons frame
button_frame = ctk.CTkFrame(root, fg_color="#1C1C1C")
button_frame.grid(row=2, column=0, pady=10)

analyze_button = ctk.CTkButton(
    button_frame,
    text="Analyze Text",
    command=analyze_text,
    width=150,
    height=40,
    fg_color="#00BFFF",
    hover_color="#0080FF",
    corner_radius=10,
)
analyze_button.grid(row=0, column=0, padx=10, pady=10)

load_button = ctk.CTkButton(
    button_frame,
    text="Load Random Sentence",
    command=load_random_sentence,
    width=200,
    height=40,
    fg_color="#32CD32",
    hover_color="#228B22",
    corner_radius=10,
)
load_button.grid(row=0, column=1, padx=10, pady=10)

# Result box (dark theme but more readable text)
result_box = scrolledtext.ScrolledText(
    root,
    wrap="word",
    width=100,
    height=12,
    font=("Consolas", 14, "bold"),
    bg="#121212",       # deep dark gray
    fg="#E0E0E0",       # bright gray-white text
    insertbackground="#00BFFF",  # cyan cursor color
    relief="flat",
    borderwidth=2,
)
result_box.grid(row=3, column=0, padx=30, pady=20, sticky="nsew")
result_box.configure(state="disabled")


# Run the app
root.mainloop()

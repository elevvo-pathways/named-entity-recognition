# 🧠 Named Entity Recognition (NER) with spaCy & CustomTkinter

A simple desktop app that performs **Named Entity Recognition (NER)** using both **model-based** and **rule-based** methods.
Built with **spaCy**, **CustomTkinter**, and the **CoNLL-2003 dataset**, this tool identifies entities such as people, organizations, and locations from text.

---

## ✨ Features

* 🔹 Supports **Model-based**, **Rule-based**, and **Combined** NER modes
* 🎨 Modern dark GUI built with **CustomTkinter**
* 📜 Load random sentences from the CoNLL-2003 dataset
* ⚙️ Includes custom entity patterns (e.g., Microsoft, Cairo University, Egypt)
* 💬 Clean output view showing recognized entities and their labels

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MinaYoussefKamal/named-entity-recognition.git
   cd named-entity-recognition

   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Download the English spaCy model:

   ```bash
   python -m spacy download en_core_web_sm
   ```

---

## 📚 Dataset

This project uses the **CoNLL-2003 dataset**, available on Kaggle:
🔗 ([https://www.kaggle.com/datasets/alaakhaled/conll003-english](https://www.kaggle.com/datasets/juliangarratt/conll2003-dataset/data))

Download the files (`eng.train`, `eng.testa`, and `eng.testb`) and place them in the same folder as `main.py`.

---

## ▶️ Usage

Run the app:

```bash
python main.py
```

Then you can:

* Type or paste any text to analyze entities
* Load random sentences from the dataset
* Switch between **Model-based**, **Rule-based**, or **Combined** NER modes

---

## 🧩 Tools & Libraries

* Python 3.x
* spaCy
* CustomTkinter
* Pandas

---

## 📸 Preview

<img width="1128" height="914" alt="2025-11-03 17_28_41-named-entity-recognition – main py" src="https://github.com/user-attachments/assets/7dbc49b8-2939-4c7a-b2cb-17238a891aca" />


---

## 📄 License

This project is for **educational purposes only**.
Dataset © Kaggle / CoNLL-2003.

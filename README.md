# Prescription_Analyzer
📌 Prescription Safety Analyzer with AI Clinical Summary
🩺 Project Overview

The Prescription Safety Analyzer is an AI-powered clinical decision support system designed to evaluate the safety of prescribed medicines.

It analyzes:

✔️ Maximum dosage limits

✔️ Ingredient validation

✔️ Drug–drug interactions

✔️ Contraindications

✔️ Clinical risk severity

Additionally, it generates a professional AI-powered clinical explanation using the Groq LLM API.

🚀 Key Features

🔍 Medicine registry validation

💊 Dosage safety verification

⚠️ Drug interaction detection

📊 Risk classification (Safe / Suspicious / Dangerous)

🤖 AI-generated clinical pharmacist summary

🌐 Deployable via Hugging Face Spaces

🛠️ Technologies Used

Python

Pandas – Data processing

Gradio – Web interface

Groq API – LLM-based clinical explanation

LLaMA 3.3 70B Versatile Model

CSV-based structured pharmaceutical database

GitHub for version control

Hugging Face Spaces for deployment

🧠 Workflow

User inputs two medicines and their doses.

System retrieves ingredient data from the medicine database.

Dosage rules are validated against safety thresholds.

Drug interaction rules are checked.

Final safety status is determined:

Safe & Original

Suspicious / Low Quality

Dangerous

AI generates a professional clinical summary.

📂 Project Structure
Prescription_Analyzer/
├── README.md
└── project/
    ├── app (1).py
    ├── logic.py
    ├── requirements.txt
    ├── medicine_database.csv
    ├── cleaned_dosage_rules.csv
    └── cleaned_interaction_rules.csv
⚠️ Disclaimer

This system is for educational and research purposes only.
It is not a substitute for professional medical advice.

🌍 Live Demo
https://huggingface.co/spaces/AwaisShinwari/prescription-analyzer


## Local setup

Install dependencies with `pip install -r project/requirements.txt`. The application entry point in this repository is `project/app (1).py`; the files described above are under `project/`.

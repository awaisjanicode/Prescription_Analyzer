import pandas as pd
import os
from groq import Groq
os.environ["GROQ_API_KEY"] = "GROQ_API_KEY"


# Load datasets - Ensure these CSVs are in the project folder
try:
    med_db = pd.read_csv('medicine_database.csv')
    dosage_rules = pd.read_csv('cleaned_dosage_rules.csv')
    interaction_rules = pd.read_csv('cleaned_interaction_rules.csv')
except FileNotFoundError:
    # Final fallback if names vary
    import glob
    def load_best_match(pattern, default):
        matches = glob.glob(pattern)
        return pd.read_csv(matches[0]) if matches else pd.read_csv(default)
    
    med_db = load_best_match('*medicine*', 'medicine_database.csv')
    dosage_rules = load_best_match('*dosage*', 'dosage_rules.csv')
    interaction_rules = load_best_match('*interaction*', 'interaction_rules.csv')

def analyze_prescription(med1_name, dose1, med2_name, dose2):
    results = []
    final_status = "Safe & Original"
    
    med1_name = str(med1_name).lower().strip()
    med2_name = str(med2_name).lower().strip() if med2_name and str(med2_name).strip() else None

    # Helper to clean logic
    def get_ingreds(name):
        res = med_db[med_db['medicine_name'] == name]
        if res.empty: return None
        ings = [res.iloc[0]['ingredient1']]
        if pd.notna(res.iloc[0]['ingredient2']):
            ings.append(res.iloc[0]['ingredient2'])
        return ings

    # Logic for Medicine 1
    ing1_list = get_ingreds(med1_name)
    if ing1_list is None:
        results.append(f"• [!] {med1_name.upper()}: Pharmaceutical product not identified in the approved registry.")
        final_status = "Suspicious / Low Quality"
        ing1_list = []
    else:
        for ing in ing1_list:
            rule = dosage_rules[dosage_rules['ingredient'] == ing]
            if not rule.empty:
                max_d = rule.iloc[0]['max_single_dose_mg']
                if dose1 > max_d:
                    results.append(f"• [CRITICAL] {ing.upper()}: Dosage ({dose1}mg) exceeds the therapeutic safety ceiling of {max_d}mg.")
                    final_status = "Dangerous"
                else:
                    results.append(f"• {ing.upper()}: Dosing parameters validated within standard clinical range.")

    # Logic for Medicine 2
    if med2_name:
        ing2_list = get_ingreds(med2_name)
        if ing2_list is None:
            results.append(f"• [!] {med2_name.upper()}: Pharmaceutical product not identified in the approved registry.")
            if final_status != "Dangerous": final_status = "Suspicious / Low Quality"
        else:
            for ing in ing2_list:
                rule2 = dosage_rules[dosage_rules['ingredient'] == ing]
                if not rule2.empty:
                    max_d2 = rule2.iloc[0]['max_single_dose_mg']
                    if dose2 > max_d2:
                        results.append(f"• [CRITICAL] {ing.upper()}: Dosage ({dose2}mg) exceeds the therapeutic safety ceiling of {max_d2}mg.")
                        final_status = "Dangerous"
            
            # Interaction Logic
            if ing1_list:
                for i1 in ing1_list:
                    for i2 in ing2_list:
                        match = interaction_rules[
                            ((interaction_rules['ingredient1'] == i1) & (interaction_rules['ingredient2'] == i2)) |
                            ((interaction_rules['ingredient1'] == i2) & (interaction_rules['ingredient2'] == i1))
                        ]
                        if not match.empty:
                            severity = match.iloc[0]['severity']
                            results.append(f"• [CONTRAINDICATION] {severity.upper()}: {match.iloc[0]['message']}")
                            if severity.lower() == "dangerous" or severity.lower() == "high":
                                final_status = "Dangerous"

    return final_status, "\n".join(results)

def get_ai_explanation(status, report):
    # API key provided by user
    api_key = "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"
    
    if not api_key: 
        return "### ⚠️ System Note\nGROQ_API_KEY not found. Please set the API key to enable AI-powered clinical summaries."

    client = Groq(api_key=api_key)
    
    prompt = f"""
    ROLE: Clinical Pharmacist Consultant
    STATUS: {status}
    TECHNICAL REPORT:
    {report}
    
    TASK: Generate a professional clinical summary for the patient. 
    STRUCTURE:
    1. **Clinical Summary**: A high-level overview.
    2. **Pharmacological Risk Assessment**: Explain risks if 'Dangerous' or 'Suspicious'.
    3. **Clinical Recommendations**: Clear expert advice.
    
    REQUIREMENTS: 
    - Formal, authoritative tone. 
    - Use markdown.
    """
    
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"### AI Analysis Unavailable\n\n**Technical Summary:**\n{report}\n\n*Error: {str(e)}*"

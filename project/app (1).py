import gradio as gr
import os
import pandas as pd
from logic import analyze_prescription, get_ai_explanation

# --- Custom Styling ---
custom_css = """
.header { text-align: center; padding: 20px; background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; border-radius: 10px; margin-bottom: 20px; }
.card { border: 1px solid #ddd; border-radius: 10px; padding: 20px; background: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
"""

def run_safety_app(med1, dose1, med2, dose2):
    if not med1:
        return "⚠️ Missing Information", "Please enter at least the first medicine name.", ""
    
    # Process through rule-based logic
    status, report = analyze_prescription(med1, dose1, med2, dose2)
    
    # Generate AI professional summary
    ai_msg = get_ai_explanation(status, report)
    
    # Format status for display
    status_icon = "✅" if "Safe" in status else "⚠️" if "Suspicious" in status else "🚨"
    formatted_status = f"{status_icon} {status.upper()}"
    
    return formatted_status, report, ai_msg

# Create Datasets view for the "Database" tab
try:
    med_db = pd.read_csv('medicine_database.csv').head(10)
    interaction_rules = pd.read_csv('cleaned_interaction_rules.csv').head(10)
except:
    med_db = pd.DataFrame({"Note": ["Database files partially missing."]})
    interaction_rules = pd.DataFrame({"Note": ["Database files partially missing."]})

with gr.Blocks(title="Medicine Safety Hub") as demo:
    # Use gr.HTML for the header to avoid gr.Div issues
    gr.HTML("""
    <div class="header">
        <h1 style="color: white; margin: 0;">🛡️ AI Medicine Safety Hub</h1>
        <p style="color: white; margin: 5px 0 0 0;">Professional Clinical Analysis Tool for Prescription Validation</p>
    </div>
    """)

    with gr.Tabs():
        with gr.TabItem("📋 Prescription Analysis"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("#### 📝 Input Prescription")
                    m1 = gr.Textbox(label="Primary Medicine", placeholder="e.g., Panadol", info="Enter the main medicine name")
                    d1 = gr.Number(label="Dosage (mg)", value=500, minimum=0)
                    
                    gr.Markdown("---")
                    
                    m2 = gr.Textbox(label="Secondary Medicine (Optional)", placeholder="e.g., Brufen", info="Enter another medicine to check interactions")
                    d2 = gr.Number(label="Dosage (mg)", value=0, minimum=0)
                    
                    btn = gr.Button("Evaluate Clinical Safety", variant="primary", size="lg")
                
                with gr.Column(scale=1.5):
                    gr.Markdown("#### 📊 Assessment Results")
                    status_out = gr.Label(label="Safety Classification")
                    
                    with gr.Accordion("Technical Report Details", open=True):
                        report_out = gr.Markdown("Analysis results will appear here...")
                    
                    gr.Markdown("#### 🤖 AI Clinical Insights")
                    ai_out = gr.Markdown("The AI will provide a professional summary after evaluation.")

        with gr.TabItem("📚 Clinical Database"):
            gr.Markdown("### Registry Snippet")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Supported Medicines")
                    gr.DataFrame(med_db)
                with gr.Column():
                    gr.Markdown("#### Known Interactions")
                    gr.DataFrame(interaction_rules)

    btn.click(
        fn=run_safety_app, 
        inputs=[m1, d1, m2, d2], 
        outputs=[status_out, report_out, ai_out]
    )

    gr.Markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em; margin-top: 30px;">
        Powered by AI Clinical Decision Support System | Professional Use Only
    </div>
    """)

if __name__ == "__main__":
    # Gradio 6.0+ compatibility: moving theme and css to launch if needed, 
    # but theme=... is usually fine in Blocks. Leaving as is but removing gr.Div.
    demo.launch(share=True)

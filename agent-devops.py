from langchain_community.llms import Ollama
from colorama import Fore, Style, init
import os
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# 1. Set up Local LLM (Ollama model)
llm = Ollama(model="llama3.2")

# 2. Define Agent Functions

def incident_analyst(logs: str) -> str:
    prompt = f"""
You are a senior Site Reliability Engineer (SRE).

Analyze the following incident logs:

{logs}

Provide:
- Root Cause Analysis (RCA)
- Immediate mitigation actions
- Long-term preventative recommendations

Structure clearly in bullet points.
"""
    analysis = llm.invoke(prompt)
    return analysis.strip()

def runbook_writer(analysis: str) -> str:
    prompt = f"""
You are a technical writer.

Using the following incident analysis:

{analysis}

Generate a detailed Incident Response Runbook in Markdown format with sections:
- Incident Summary
- Root Cause
- Immediate Actions
- Long-term Actions
- Lessons Learned
"""
    runbook = llm.invoke(prompt)
    return runbook.strip()

# 3. Helper Function: Load sample logs
def load_logs(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 4. Main Orchestration

if __name__ == "__main__":
    print(Fore.CYAN + "=== DevOps Incident Analyst AI ===\n")
    
    # Load sample incident logs
    log_file = "sample_logs/pod_crash_log.txt"  # Example path
    if not os.path.exists(log_file):
        print(Fore.RED + f"Log file {log_file} not found!")
        exit(1)

    logs = load_logs(log_file)

    # Step 1: Incident Analysis
    print(Fore.YELLOW + ">> Agent: Incident Analyst\n")
    print(Fore.YELLOW + ">> Task: Analyzing Incident Logs...\n")
    incident_analysis = incident_analyst(logs)
    print(Fore.GREEN + "--- Incident Analysis Output [Incident Analyst Agent] ---\n")
    print(incident_analysis)
    print("\n" + "="*80 + "\n")

    # Step 2: Runbook Creation
    print(Fore.YELLOW + ">> Agent: Runbook Writer\n")
    print(Fore.YELLOW + ">> Task: Creating Incident Runbook...\n")
    incident_runbook = runbook_writer(incident_analysis)
    print(Fore.GREEN + "--- Incident Runbook Output [Runbook Writer Agent] ---\n")
    print(incident_runbook)
    print("\n" + "="*80 + "\n")

    # Step 3: Save the Outputs
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    with open(os.path.join(output_dir, f"incident_analysis_{current_date}.md"), "w", encoding="utf-8") as f:
        f.write("# Incident Analysis\n\n" + incident_analysis)

    with open(os.path.join(output_dir, f"incident_runbook_{current_date}.md"), "w", encoding="utf-8") as f:
        f.write("# Incident Response Runbook\n\n" + incident_runbook)

    print(Fore.CYAN + f"✅ Incident Analysis and Runbook saved to '{output_dir}' folder.\n")
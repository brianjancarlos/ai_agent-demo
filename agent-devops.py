from langchain_ollama import OllamaLLM
from colorama import Fore, Style, init
import os
from datetime import datetime
import sys

# Initialize colorama
init(autoreset=True)

# 1. Set up Local LLM (Ollama model)
llm = OllamaLLM(model="qwen3:4b")

def process_stream(prompt):
    full_response = []
    buffer = ""
    for chunk in llm.stream(prompt):
        chunk_text = chunk
        # Color thinking lines in magenta
        if "🤔 Thinking:" in chunk_text:
            chunk_text = f"{Fore.MAGENTA}{chunk_text}{Style.RESET_ALL}"
        elif "🤔 Planning:" in chunk_text:
            chunk_text = f"{Fore.MAGENTA}{chunk_text}{Style.RESET_ALL}"
        
        print(chunk_text, end='', flush=True)
        full_response.append(chunk_text)
    return ''.join(full_response)

# 2. Define Agent Functions

def incident_analyst(logs: str) -> str:
    prompt = f"""
You are a senior Site Reliability Engineer (SRE).
Important: Each step of your thought process must be on a new line.
Show your thought process step by step as you analyze these logs.

For each step, prefix with "🤔 Thinking: " to show your reasoning.

Analyze the following incident logs:

{logs}

Provide:
1. First share your thought process
2. Then provide:
   - Root Cause Analysis (RCA)
   - Immediate mitigation actions
   - Long-term preventative recommendations

Structure the final analysis in bullet points.
"""
    print(Fore.CYAN + "\n=== Incident Analysis Thinking Process ===\n")
    analysis = process_stream(prompt)
    return analysis.strip()

def runbook_writer(analysis: str) -> str:
    prompt = f"""
You are a technical writer.
Important: Each planning step must be on a new line.
Show your thought process as you create this runbook.

For each section you plan, prefix with "🤔 Planning: " to show your reasoning.

Using the following incident analysis:

{analysis}

Generate a detailed Incident Response Runbook in Markdown format with sections:
1. First share your section planning process
2. Then write the full runbook with:
   - Incident Summary
   - Root Cause  
   - Immediate Actions
   - Long-term Actions
   - Lessons Learned
"""
    print(Fore.CYAN + "\n=== Runbook Creation Thinking Process ===\n")
    runbook = process_stream(prompt)
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
    print(Fore.GREEN + "\n--- Final Incident Analysis ---\n")
    print(incident_analysis)
    print("\n" + "="*80 + "\n")

    # Step 2: Runbook Creation
    print(Fore.YELLOW + ">> Agent: Runbook Writer\n")
    print(Fore.YELLOW + ">> Task: Creating Incident Runbook...\n")
    incident_runbook = runbook_writer(incident_analysis)
    print(Fore.GREEN + "\n--- Final Runbook ---\n")
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
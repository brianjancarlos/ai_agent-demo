import os
import configparser
from datetime import datetime
from src.agents.devops import IncidentAnalyst, RunbookWriter
from src.core.pipeline import Pipeline
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def load_logs(file_path: str) -> str:
    """Load logs from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    devops_model = config.get('llm', 'devops_model')
    log_file = config.get('settings', 'log_file')
    output_dir = config.get('settings', 'output_dir')

    print(Fore.CYAN + "=== DevOps Incident Analyst AI ===")

    # Check if log file exists
    if not os.path.exists(log_file):
        print(Fore.RED + f"Log file {log_file} not found!")
        exit(1)

    # Load logs
    logs = load_logs(log_file)

    # 1. Define Agents
    incident_analyst = IncidentAnalyst(model=devops_model)
    runbook_writer = RunbookWriter(model=devops_model)

    # 2. Create and run pipeline
    devops_pipeline = Pipeline()
    devops_pipeline.add_step(incident_analyst, "analyze_logs", "incident_analysis")
    devops_pipeline.add_step(runbook_writer, "create_runbook", "incident_runbook")

    # The initial key in the dictionary should match what the first agent expects.
    # In this case, the `analyze_logs` method expects a 'logs' argument.
    # We'll pass the analysis to the next step.
    results = devops_pipeline.run(initial_data={"logs": logs})

    # The 'run' method now returns a dictionary with all the intermediate results.
    incident_analysis = results.get("incident_analysis", "")
    incident_runbook = results.get("incident_runbook", "")


    # 3. Save outputs
    os.makedirs(output_dir, exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d")

    analysis_path = os.path.join(output_dir, f"incident_analysis_{current_date}.md")
    runbook_path = os.path.join(output__dir, f"incident_runbook_{current_date}.md")

    with open(analysis_path, "w", encoding="utf-8") as f:
        f.write("# Incident Analysis\n\n" + incident_analysis)

    with open(runbook_path, "w", encoding="utf-8") as f:
        f.write("# Incident Response Runbook\n\n" + incident_runbook)

    print(Fore.CYAN + f"\n✅ Incident Analysis and Runbook saved to '{output_dir}' folder.")

if __name__ == "__main__":
    main()

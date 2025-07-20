from src.core.agent import Agent

class IncidentAnalyst(Agent):
    def __init__(self, model: str):
        system_prompt = """
You are a senior Site Reliability Engineer (SRE).
Important: Each step of your thought process must be on a new line.
Show your thought process step by step as you analyze logs.

For each step, prefix with "🤔 Thinking: " to show your reasoning.

Provide:
1. First share your thought process
2. Then provide:
   - Root Cause Analysis (RCA)
   - Immediate mitigation actions
   - Long-term preventative recommendations

Structure the final analysis in bullet points.
"""
        super().__init__(name="Incident Analyst", model=model, system_prompt=system_prompt)
        self.icon = "🕵️"

    def analyze_logs(self, logs: str) -> str:
        prompt = f"Analyze the following incident logs:\n\n{logs}"
        return self.stream(prompt)

class RunbookWriter(Agent):
    def __init__(self, model: str):
        system_prompt = """
You are a technical writer.
Important: Each planning step must be on a new line.
Show your thought process as you create this runbook.

For each section you plan, prefix with "🤔 Planning: " to show your reasoning.

Generate a detailed Incident Response Runbook in Markdown format with sections:
1. First share your section planning process
2. Then write the full runbook with:
   - Incident Summary
   - Root Cause
   - Immediate Actions
   - Long-term Actions
   - Lessons Learned
"""
        super().__init__(name="Runbook Writer", model=model, system_prompt=system_prompt)
        self.icon = "✍️"

    def create_runbook(self, analysis: str) -> str:
        prompt = f"Using the following incident analysis:\n\n{analysis}"
        return self.stream(prompt)

# AI Agent Demo

A collection of AI agents for research and DevOps automation tasks.

## Features

- Research Agent: Performs web research, writing, and editing on specified topics
- DevOps Agent: Analyzes incident logs and generates runbooks

## Installation

1. Install required dependencies:

```bash
pip install duckduckgo-search  # For web search capabilities
pip install colorama          # For colored console output
pip install langchain_community  # For LLM interactions
```

## Usage

### Research Agent

Run the research agent:

```bash
python agent-simple_research.py
```

### DevOps Agent

Run the DevOps incident analysis:

```bash
python agent-devops.py
```

## Project Structure

```
.
├── agent-simple_research.py  # Research agent implementation
├── agent-devops.py          # DevOps agent implementation
├── sample_logs/             # Sample incident logs
└── outputs/                 # Generated analysis and runbooks
```

## Requirements

- Python 3.8+
- Ollama with LLM models installed

import configparser
from src.agents.research import Researcher, Writer, Editor
from src.core.pipeline import Pipeline
from colorama import Fore, init, Style

# Initialize colorama
init(autoreset=True)

def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    research_model = config.get('llm', 'research_model')
    topic = config.get('settings', 'research_topic')

    print(f"\n{Fore.CYAN}Starting Research Pipeline for:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{topic}{Style.RESET_ALL}\n")

    # 1. Define Agents
    researcher = Researcher(model=research_model)
    writer = Writer(model=research_model)
    editor = Editor(model=research_model)

    # 2. Create and run pipeline
    research_pipeline = Pipeline()
    research_pipeline.add_step(researcher, "research", "research_notes")
    research_pipeline.add_step(writer, "write_article", "article_draft")
    research_pipeline.add_step(editor, "edit_article", "final_article")

    results = research_pipeline.run(initial_data={"topic": topic})

    # 3. Save output
    final_article = results.get("final_article", "")
    references = researcher.references # Get references from the researcher agent

    with open("final_article.md", "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{final_article}\n\n## References\n\n")
        for ref in references:
            f.write(f"{ref}\n")

    print(f"\n{Fore.GREEN}✅ Process Complete! Final article saved to final_article.md{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

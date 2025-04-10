from langchain_community.llms import Ollama
from colorama import init, Fore, Style
from tqdm import tqdm
from duckduckgo_search import DDGS
import time
from datetime import datetime
from urllib.parse import urlparse

# Initialize colorama
init()

# Helper function for progress indication
def show_progress(description, duration=2):
    with tqdm(total=100, desc=description, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for i in range(10):
            time.sleep(duration / 10)
            pbar.update(10)

def format_agent_message(agent_name, message):
    """Format message with agent name"""
    agent_icons = {
        "Researcher": "🔎",
        "Writer": "✍️",
        "Editor": "✨"
    }
    icon = agent_icons.get(agent_name, "🤖")
    return f"\n{Fore.CYAN}[{icon} {agent_name} Agent]{Style.RESET_ALL}\n{message}"

# 1. Setup LLM
llm = Ollama(model="llama3.2")  # You can change model here

# 2. Define Agent Functions

def format_apa_reference(title, url, accessed_date=None):
    """Format a web reference in APA style"""
    if accessed_date is None:
        accessed_date = datetime.now()
    
    domain = urlparse(url).netloc
    author = domain.replace('www.', '')
    
    return f"{author}. ({accessed_date.year}). {title}. Retrieved {accessed_date.strftime('%B %d, %Y')}, from {url}"

def researcher(topic):
    show_progress(f"{Fore.BLUE}🔎 Searching the web{Style.RESET_ALL}")
    
    # Perform web search
    search_results = []
    references = []
    current_date = datetime.now()
    
    with DDGS() as ddgs:
        for r in ddgs.text(topic, max_results=5):
            search_results.append(f"- {r['title']}: {r['body']}")
            # Store reference information
            if 'link' in r:
                references.append(format_apa_reference(r['title'], r['link'], current_date))
    
    web_research = "\n".join(search_results)
    
    show_progress(f"{Fore.BLUE}🔎 Analyzing findings{Style.RESET_ALL}")
    prompt = f"""
You are a researcher. Based on these search results and your knowledge, analyze and summarize key points about:
{topic}

Search Results:
{web_research}

Summarize your findings in bullet points, combining the search results with your knowledge.
"""
    research_summary = llm.invoke(prompt)
    return format_agent_message("Researcher", research_summary.strip()), references

def writer(research_summary):
    show_progress(f"{Fore.BLUE}✍️ Writing{Style.RESET_ALL}")
    # Remove any agent formatting for the prompt
    clean_summary = research_summary.replace(f"{Fore.CYAN}", "").replace(f"{Style.RESET_ALL}", "")
    prompt = f"""
You are a writer. Based on the following research notes:

{clean_summary}

Write a detailed, engaging article. Use clear headings and paragraphs.
"""
    article = llm.invoke(prompt)
    return format_agent_message("Writer", article.strip())

def editor(article):
    show_progress(f"{Fore.BLUE}✨ Editing{Style.RESET_ALL}")
    # Remove any agent formatting for the prompt
    clean_article = article.replace(f"{Fore.CYAN}", "").replace(f"{Style.RESET_ALL}", "")
    prompt = f"""
You are an editor. Please edit the following article for:
- Grammar
- Clarity
- Flow

Article:

{clean_article}

Return the improved article.
"""
    edited_article = llm.invoke(prompt)
    return format_agent_message("Editor", edited_article.strip())

# 3. Main Flow

if __name__ == "__main__":
    # Choose your topic
    topic = "The Future of Renewable Energy Technologies in 2030"

    print(f"\n{Fore.CYAN}Starting Research Pipeline for:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{topic}{Style.RESET_ALL}\n")

    # Progress tracking
    total_steps = 3
    current_step = 1

    # Research phase
    print(f"\n[{current_step}/{total_steps}] {Fore.BLUE}Research Phase{Style.RESET_ALL}")
    research_notes, references = researcher(topic)
    print(f"{Fore.GREEN}📝 Research Summary:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{research_notes}{Style.RESET_ALL}\n")
    current_step += 1

    # Writing phase
    print(f"\n[{current_step}/{total_steps}] {Fore.BLUE}Writing Phase{Style.RESET_ALL}")
    article_draft = writer(research_notes)
    print(f"{Fore.GREEN}📄 Draft Article:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{article_draft}{Style.RESET_ALL}\n")
    current_step += 1

    # Editing phase
    print(f"\n[{current_step}/{total_steps}] {Fore.BLUE}Editing Phase{Style.RESET_ALL}")
    final_article = editor(article_draft)
    print(f"{Fore.GREEN}📚 Final Article:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{final_article}{Style.RESET_ALL}\n")

    # Save output with references
    with open("final_article.md", "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{final_article}\n\n## References\n\n")
        for ref in references:
            f.write(f"{ref}\n")

    print(f"\n{Fore.GREEN}✅ Process Complete! Final article saved to final_article.md{Style.RESET_ALL}")
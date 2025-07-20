from src.core.agent import Agent
from duckduckgo_search import DDGS
from datetime import datetime
from urllib.parse import urlparse

class Researcher(Agent):
    def __init__(self, model: str):
        system_prompt = "You are a researcher. Based on search results and your knowledge, analyze and summarize key points."
        super().__init__(name="Researcher", model=model, system_prompt=system_prompt)
        self.icon = "🔎"
        self.references = []

    def _format_apa_reference(self, title, url, accessed_date=None):
        """Format a web reference in APA style"""
        if accessed_date is None:
            accessed_date = datetime.now()

        domain = urlparse(url).netloc
        author = domain.replace('www.', '')

        return f"{author}. ({accessed_date.year}). {title}. Retrieved {accessed_date.strftime('%B %d, %Y')}, from {url}"

    def research(self, topic: str) -> str:
        search_results = []
        self.references = []
        current_date = datetime.now()

        with DDGS() as ddgs:
            for r in ddgs.text(topic, max_results=5):
                search_results.append(f"- {r['title']}: {r['body']}")
                if 'link' in r:
                    self.references.append(self._format_apa_reference(r['title'], r['link'], current_date))

        web_research = "\n".join(search_results)
        prompt = f"Topic: {topic}\n\nSearch Results:\n{web_research}\n\nSummarize your findings in bullet points."
        return self.invoke(prompt)

class Writer(Agent):
    def __init__(self, model: str):
        system_prompt = "You are a writer. Write a detailed, engaging article based on the provided research notes."
        super().__init__(name="Writer", model=model, system_prompt=system_prompt)
        self.icon = "✍️"

    def write_article(self, research_summary: str) -> str:
        prompt = f"Research notes:\n\n{research_summary}"
        return self.invoke(prompt)

class Editor(Agent):
    def __init__(self, model: str):
        system_prompt = "You are an editor. Please edit the following article for grammar, clarity, and flow."
        super().__init__(name="Editor", model=model, system_prompt=system_prompt)
        self.icon = "✨"

    def edit_article(self, article: str) -> str:
        prompt = f"Article:\n\n{article}"
        return self.invoke(prompt)

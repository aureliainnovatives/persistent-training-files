import os
from pathlib import Path
from typing import Any
import yaml
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


CATALOG_FILE = Path(__file__).with_name("api-catalog.yaml")


def load_catalog() -> dict[str, Any]:
    with CATALOG_FILE.open(encoding="utf-8") as f:
        return yaml.safe_load(f)





@tool
def list_apis() -> str:
    """List known APIs with domain and purpose."""
    c = load_catalog()
    return "\n".join(
        f"{a['id']} | {a['name']} | {a['domain']} | {a['purpose']}"
        for a in c["apis"]
    )
# We are choosing Lexical search (Keyword search) as the search strategy.
# BM25 is a popular ranking function that is used in Elasticsearch.
@tool
def search_apis(query: str) -> str:
    """Search the API catalog for capabilities relevant to a business query."""
    c = load_catalog()
    words = {w.lower().strip(".,") for w in query.split() if len(w) > 3}
    scored = []
    for a in c["apis"]:
        text = f"{a['id']} {a['name']} {a['domain']} {a['purpose']}".lower()
        score = sum(w in text for w in words)
        if score:
            scored.append((score, a))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return "No direct keyword match. Catalog:\n" + "\n".join(
            f"- {a['id']}: {a['purpose']}" for a in c["apis"]
        )
    return "\n".join(
        f"{a['id']} | {a['name']} | {a['purpose']}" for _, a in scored
    )

@tool
def get_api_details(api_id: str) -> str:
    """Return metadata for one API."""
    for a in load_catalog()["apis"]:
        if a["id"].lower() == api_id.lower():
            return yaml.safe_dump(a, sort_keys=False)
    return f"API '{api_id}' not found."

@tool
def get_dependencies(api_id: str) -> str:
    """Return known upstream dependencies and downstream consumers."""
    dep = load_catalog().get("dependencies", {}).get(api_id)
    if not dep:
        return f"No dependency record for '{api_id}'."
    return yaml.safe_dump({"api_id": api_id, **dep}, sort_keys=False)

@tool
def find_consumers(api_id: str) -> str:
    """Return known direct consumers for change-impact analysis."""
    dep = load_catalog().get("dependencies", {}).get(api_id)
    if not dep:
        return f"No dependency record for '{api_id}'."
    consumers = dep.get("consumed_by", [])
    return "Known consumers:\n" + "\n".join(f"- {x}" for x in consumers)

@tool
def find_reuse_candidates(requirement: str) -> str:
    """Find existing APIs that might satisfy a proposed new capability."""
    c = load_catalog()
    words = {w.lower().strip(".,") for w in requirement.split() if len(w) > 3}
    scored = []
    for a in c["apis"]:
        text = f"{a['name']} {a['domain']} {a['purpose']}".lower()
        score = sum(w in text for w in words)
        if score:
            scored.append((score, a))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return "No direct reuse candidate found; inspect the full catalog before creating a new API."
    return "\n".join(
        f"{a['id']} | {a['name']} | {a['purpose']}" for _, a in scored
    )


SYSTEM_PROMPT = """
You are an API Catalog Intelligence Agent assisting an Integration Architect.

Use tools to:
- discover existing APIs from business intent,
- recommend relevant APIs,
- inspect dependencies and consumers,
- assess possible change impact,
- identify reuse candidates before new APIs are created.

Guardrails:
- api-catalog.yaml is the source of truth for known enterprise facts.
- Never invent APIs, owners, dependencies or consumers.
- Clearly separate CONFIRMED catalog facts from POSSIBLE implications.
- For impact questions, inspect dependency information first.
- Semantic similarity suggests investigation; it does not prove equivalence.
"""

model = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0,
)


agent = create_agent(
    model=model,
    tools=[list_apis, search_apis, get_api_details,
           get_dependencies, find_consumers, find_reuse_candidates],
    system_prompt=SYSTEM_PROMPT,
)

def ask(question: str) -> None:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print("\nAGENT RESPONSE\n" + "-" * 60)
    print(result["messages"][-1].content)
    print("-" * 60)

if __name__ == "__main__":

    print("API Catalog Intelligence Agent")
    print("=" * 60)

    while True:
        question = input("Enter a question: ")
        ask(question)
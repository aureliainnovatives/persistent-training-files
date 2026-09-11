# Module 3.2 — Multi-Agent Demos with `.env` Configuration

All eight demos now load model configuration from a `.env` file.

## 1. Install

Each demo contains its own pip command. `python-dotenv` is now included.

## 2. Create `.env`

Copy:

```bash
cp .env.example .env
```

Then edit:

```env
OPENAI_API_KEY=your-real-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
```

`OPENAI_BASE_URL` deliberately uses the standard OpenAI endpoint by default.

## 3. Switching providers later

If an alternative provider exposes an OpenAI-compatible API, normally only these values need to change:

```env
OPENAI_API_KEY=provider-key
OPENAI_BASE_URL=https://provider-specific-base-url/v1
OPENAI_MODEL=provider-model-name
```

The intention is to keep credentials and provider endpoint configuration outside the Python source.

## Files

1. `01_langchain_supervisor.py`
2. `02_langchain_router.py`
3. `03_langgraph_incident_graph.py`
4. `04_langgraph_conditional_escalation.py`
5. `05_autogen_round_robin.py`
6. `06_autogen_selector.py`
7. `07_crewai_sequential.py`
8. `08_crewai_hierarchical.py`

> Demo 04 does not actually call an LLM, but it retains the same configuration structure only where applicable in the generated source.

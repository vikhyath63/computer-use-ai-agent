# Computer-Use AI Agent

A browser automation service with a strict host allow-list and explicit action sequence. It uses Playwright to navigate, click, type and capture screenshots. The first version is a deterministic browser-control harness; vision-based element grounding and an LLM policy can be plugged in later.

## Setup
```bash
pip install -e ".[dev]"
playwright install chromium
uvicorn app.main:app --reload
```
Open /docs. Set `ALLOWED_HOSTS=example.com,playwright.dev` before running. Do not expose this service publicly: browser automation can perform real actions.

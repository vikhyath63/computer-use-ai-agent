import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.browser import execute_steps
app=FastAPI(title="Computer-Use AI Agent",version="0.1.0")
ALLOWED={h.strip().lower() for h in os.getenv("ALLOWED_HOSTS","example.com").split(",") if h.strip()}
class RunRequest(BaseModel): url: str; steps: list[dict]=Field(default_factory=list,max_length=12)
@app.get("/health")
def health(): return {"status":"ok","allowed_hosts":sorted(ALLOWED)}
@app.post("/run")
async def run(req:RunRequest):
    try: return await execute_steps(req.url,req.steps,ALLOWED)
    except Exception as exc: raise HTTPException(400,str(exc)) from exc

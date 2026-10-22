"""Simple MVP: Text Processor Service."""
import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="TextProcessor MVP")

class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Input text")
    operation: str = Field(default="uppercase", description="Operation: uppercase, lowercase, reverse")

class ProcessResponse(BaseModel):
    result: str
    operation: str
    length: int

class Agent:
    """Internal agent that processes text."""
    def __init__(self, name: str):
        self.name = name
        self.cache: Dict[str, str] = {}

    def execute(self, text: str, operation: str) -> str:
        """Process text based on operation."""
        cache_key = f"{text}:{operation}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if operation == "uppercase":
            res = text.upper()
        elif operation == "lowercase":
            res = text.lower()
        elif operation == "reverse":
            res = text[::-1]
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        self.cache[cache_key] = res
        return res

def demo() -> str:
    """Run a demo execution and return the result string."""
    agent = Agent("demo_agent")
    result = agent.execute("Hello World", "uppercase")
    return f"Final Output: {result}"

@app.post("/process", response_model=ProcessResponse)
def process_text(req: ProcessRequest):
    """API endpoint to process text."""
    try:
        agent = Agent("api_agent")
        res = agent.execute(req.text, req.operation)
        return ProcessResponse(result=res, operation=req.operation, length=len(res))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

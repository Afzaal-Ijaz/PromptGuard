from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from promptguard.middleware import GuardMiddleware

app = FastAPI(title="LLM-Flow Testing App")

# secure the entire API
app.add_middleware(GuardMiddleware)


class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Ye ek dummy endpoint hai. 
    Asal production app mein yahan OpenAI ya Claude ka code hota hai.
    """
    safe_prompt = request.prompt
    
    return {
        "status": "success",
        "message": "Request reached the API endpoint securely.",
        "final_prompt_received_by_llm": safe_prompt
    }

if __name__ == "__main__":
    print("Starting FastAPI server with LLM-Flow Security...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
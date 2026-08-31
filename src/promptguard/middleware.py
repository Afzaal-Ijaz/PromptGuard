from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import json

from promptguard.core.engine import SecurityEngine

class GuardMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.engine = SecurityEngine()

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.headers.get("content-type") == "application/json":
            try:
                body_bytes = await request.body()
                body_json = json.loads(body_bytes.decode("utf-8"))
                user_prompt = body_json.get("prompt", "")
                
                if user_prompt:
                    input_scan = self.engine.scan_input(user_prompt)
                    
                    if input_scan["status"] == "blocked":
                        return JSONResponse(
                            status_code=400,
                            content={"error": input_scan["reason"]}
                        )
                    
                    body_json["prompt"] = input_scan["safe_prompt"]
                    
                    async def receive():
                        return {"type": "http.request", "body": json.dumps(body_json).encode("utf-8")}
                    request._receive = receive

            except json.JSONDecodeError:
                pass 
        response = await call_next(request)
        

        return response
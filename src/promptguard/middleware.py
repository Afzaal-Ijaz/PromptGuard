from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import json

from promptguard.core.engine import SecurityEngine


class GuardMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.engine = SecurityEngine()

    async def dispatch(self, request: Request, call_next):
        content_type = request.headers.get("content-type", "")

        if request.method == "POST" and "application/json" in content_type:
            try:
                body = json.loads((await request.body()).decode("utf-8"))
                prompt = body.get("prompt", "")

                if prompt:
                    result = self.engine.scan_input(prompt)

                    if result["status"] == "blocked":
                        return JSONResponse(
                            status_code=400,
                            content={"error": result["reason"]},
                        )

                    body["prompt"] = result["safe_prompt"]

                    async def receive():
                        return {
                            "type": "http.request",
                            "body": json.dumps(body).encode("utf-8"),
                        }

                    request._receive = receive

            except json.JSONDecodeError:
                pass

        return await call_next(request)

# 🛡️ LLM-Flow (PromptGuard)

PromptGuard is a lightweight, plug-and-play security middleware for LLM-based applications. It sits between your users and your LLM API to detect prompt injections, redact Personally Identifiable Information (PII), and filter toxic outputs—ensuring enterprise-grade AI safety with just a few lines of code.

---

## 🚀 Why PromptGuard?

As AI agents and RAG systems move to production, security is often an afterthought. PromptGuard solves three major vulnerabilities:
1. **Prompt Injection (Jailbreaking):** Prevents users from overriding system instructions.
2. **PII Leakage:** Automatically redacts sensitive data (Credit Cards, SSNs, Emails) before it reaches third-party LLM providers.
3. **Output Toxicity:** Validates the LLM's response to ensure safe and compliant delivery to the user.

## 🛠️ Features (Planned)
- [x] Initial Architecture & Scaffolding
- [ ] **PII Redaction Engine** (Powered by Microsoft Presidio)
- [ ] **Injection Detection** (Powered by Hugging Face / PyTorch)
- [ ] **Toxicity Validation** (Output filtering)
- [ ] **FastAPI Middleware Integration**

## 📦 Installation

*(Note: PromptGuard is currently under active development. Installation via PyPI will be available soon.)*

If you are building from the source, we recommend using `uv` for lightning-fast dependency management:

```bash
uv add fastapi pydantic presidio-analyzer presidio-anonymizer transformers torch spacy
uv run python -m spacy download en_core_web_sm
💻 Quick Start (Expected Usage)
Integrating PromptGuard into your FastAPI application will be as simple as adding a middleware:

Python
from fastapi import FastAPI
from promptguard.middleware import GuardMiddleware

app = FastAPI()

# Add PromptGuard Security Layer
app.add_middleware(
    GuardMiddleware,
    detect_injection=True,
    redact_pii=True,
    filter_toxicity=True
)

@app.post("/chat")
async def chat_endpoint(prompt: str):
    # Your prompt is now safe from injections and PII leaks!
    response = call_llm_api(prompt)
    return {"response": response}
🏗️ Architecture
PromptGuard processes data in three phases:

Pre-LLM: Intercepts user prompts, scans for jailbreaks, and anonymizes sensitive data.

LLM Call: Forwards the sanitized prompt to your AI model (OpenAI, Claude, etc.).

Post-LLM: Validates the generated response for safety policies before returning it to the user.

🤝 Contributing
Contributions are welcome! Please check the issues page or submit a pull request if you want to help improve LLM security.

📄 License
This project is licensed under the MIT License.
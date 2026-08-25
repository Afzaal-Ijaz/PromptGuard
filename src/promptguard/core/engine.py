from promptguard.scanners.pii import PIIScanner
from promptguard.scanners.injection import InjectionScanner
from promptguard.scanners.toxicity import ToxicityScanner

class SecurityEngine:
    def __init__(self):
        """
        Engine initialize hote hi teeno models (PII, Injection, Toxicity) ko RAM mein load kar lega.
        """
        print("Loading Security Engine and Models... Please wait.")
        self.pii_scanner = PIIScanner()
        self.injection_scanner = InjectionScanner()
        self.toxicity_scanner = ToxicityScanner()
        print("✅ Security Engine Ready!")

    def scan_input(self, prompt: str) -> dict:
        """
        Pre-LLM Phase: Ye API call hone se pehle chalega.
        Pehle hack check karega, agar safe hai toh PII hide karega.
        """
        # 1. Injection (Jailbreak) Check
        if self.injection_scanner.is_injection(prompt):
            return {
                "status": "blocked", 
                "reason": "Security Alert: Prompt Injection Detected", 
                "safe_prompt": None
            }
        
        # 2. PII Redaction 
        safe_prompt = self.pii_scanner.redact_text(prompt)
        
        return {
            "status": "passed", 
            "safe_prompt": safe_prompt
        }

    def scan_output(self, response: str) -> dict:
        """
        Post-LLM Phase: Ye LLM ke jawab dene ke baad chalega taake user ko safe text mile.
        """
        # 3. Toxicity Check
        if self.toxicity_scanner.is_toxic(response):
            return {
                "status": "blocked", 
                "reason": "Security Alert: Toxic Output Detected",
                "safe_response": None
            }
        
        return {
            "status": "passed", 
            "safe_response": response
        }
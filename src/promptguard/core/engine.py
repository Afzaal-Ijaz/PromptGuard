from promptguard.scanners.pii import PIIScanner
from promptguard.scanners.injection import InjectionScanner
from promptguard.scanners.toxicity import ToxicityScanner


class SecurityEngine:
    def __init__(self):
        # pehle None — pehli request pe load hoga
        self.pii_scanner = None
        self.injection_scanner = None
        self.toxicity_scanner = None
        print("Security Engine ready (models load on first use).")

    def _get_pii(self):
        if self.pii_scanner is None:
            print("Loading PII model...")
            self.pii_scanner = PIIScanner()
        return self.pii_scanner

    def _get_injection(self):
        if self.injection_scanner is None:
            print("Loading Injection model...")
            self.injection_scanner = InjectionScanner()
        return self.injection_scanner

    def _get_toxicity(self):
        if self.toxicity_scanner is None:
            print("Loading Toxicity model...")
            self.toxicity_scanner = ToxicityScanner()
        return self.toxicity_scanner

    def scan_input(self, prompt: str) -> dict:
        """Pre-LLM: pehle injection check, phir PII hide."""
        if self._get_injection().is_injection(prompt):
            return {
                "status": "blocked",
                "reason": "Security Alert: Prompt Injection Detected",
                "safe_prompt": None,
            }

        safe_prompt = self._get_pii().redact_text(prompt)
        return {"status": "passed", "safe_prompt": safe_prompt}

    def scan_output(self, response: str) -> dict:
        """Post-LLM: toxic reply block karo."""
        if self._get_toxicity().is_toxic(response):
            return {
                "status": "blocked",
                "reason": "Security Alert: Toxic Output Detected",
                "safe_response": None,
            }

        return {"status": "passed", "safe_response": response}

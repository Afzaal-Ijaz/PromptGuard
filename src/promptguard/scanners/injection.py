from transformers import pipeline

class InjectionScanner:
    def __init__(self, threshold: float = 0.7):
        """
        Initialize the Hugging Face text-classification pipeline.
        Model: 'ProtectAI/deberta-v3-base-prompt-injection-v2' (Industry standard for AI security)
        """
        self.threshold = threshold
        
        # The model will be downloaded the first time it runs (RAM/Storage use)
        self.classifier = pipeline(
            "text-classification", 
            model="ProtectAI/deberta-v3-base-prompt-injection-v2",
            truncation=True,
            max_length=512
        )

    def is_injection(self, text: str) -> bool:
        """
        Check  prompt  malicious hacking attempt .
        True = Hacking attempt detected (Block it)
        False = Safe prompt (Allow it)
        """
        if not text:
            return False

        result = self.classifier(text)[0]
        
        label = result['label']
        score = result['score']

        if label == "INJECTION" and score >= self.threshold:
            return True
            
        return False
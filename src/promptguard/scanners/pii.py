from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIIScanner:
    def __init__(self):
        """
        Initialize the Presidio Analyzer and Anonymizer engines.
        """
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def redact_text(self, text: str) -> str:
        """
        Scan the user's prompt or LLM response for sensitive data (PII) and hide it.
        """
        if not text:
            return text

        # Analyze the text and find where the PII (Email, Phone, Credit Card) is
        analyzer_results = self.analyzer.analyze(text=text, language='en')

        # Hide (redact) the PII
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results
        )

        return anonymized_result.text




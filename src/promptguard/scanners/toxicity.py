from transformers import pipeline

class ToxicityScanner:
    def __init__(self, threshold: float = 0.8):
        """
        Initialize a lightweight toxicity detection model.
        Model: 'martin-ha/toxic-comment-model' (DistilBERT-based, blazing fast)
        """
        self.threshold = threshold
        
        self.classifier = pipeline(
            "text-classification", 
            model="martin-ha/toxic-comment-model",
            truncation=True,
            max_length=512
        )

    def is_toxic(self, text: str) -> bool:
        """
        Check karta hai ke LLM ka response toxic ya abusive toh nahi.
        True = Toxic response (Block it)
        False = Safe response (Allow it)
        """
        if not text:
            return False

        result = self.classifier(text)[0]
        label = result['label']
        score = result['score']

        if label == "toxic" and score >= self.threshold:
            return True
            
        return False
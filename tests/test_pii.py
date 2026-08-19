from promptguard.scanners.pii import PIIScanner

def test_pii_redaction():
    # Initialize the scanner
    scanner = PIIScanner()
    
    # Test 1: Email Redaction
    text_with_email = "Hi, my secret email is john.doe@apple.com, please don't share it."
    result1 = scanner.redact_text(text_with_email)
    assert "john.doe@apple.com" not in result1
    assert "<EMAIL_ADDRESS>" in result1
    print("\nTest 1 Passed: Email successfully hidden! ->", result1)

    # Test 2: Phone Number Redaction
    text_with_phone = "You can call me at 415-555-1234 tomorrow."
    result2 = scanner.redact_text(text_with_phone)
    assert "415-555-1234" not in result2
    print("Test 2 Passed: Phone number successfully hidden! ->", result2)

    # Test 3: Safe Prompt
    safe_text = "What is the capital of France?"
    result3 = scanner.redact_text(safe_text)
    assert result3 == safe_text
    print("Test 3 Passed: Safe text remained unchanged! ->", result3)
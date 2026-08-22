from promptguard.scanners.toxicity import ToxicityScanner

def test_toxicity_detection():
    print("\nInitializing Toxicity Model... (First run downloads the model)")
    scanner = ToxicityScanner()
    
    # Test 1: Safe Output
    safe_text = "Here is the summary of the financial report you requested."
    assert scanner.is_toxic(safe_text) == False
    print("Test 1 Passed: Safe text allowed!")

    # Test 2: Toxic Output (Simulated)
    toxic_text = "You are completely stupid and this is garbage."
    assert scanner.is_toxic(toxic_text) == True
    print("Test 2 Passed: Toxic output successfully blocked!")
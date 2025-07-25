#!/usr/bin/env python3
"""
Test program to compare phonemization results between ja_original and ja modules.
Reads lines from test_prompts.txt and phonemizes each line using both modules.
"""

import sys
from misaki.ja_original import JAG2P as JAG2P_Original
from misaki.ja import JAG2P as JAG2P_New

def test_phonemization_comparison():
    """Test phonemization differences between ja_original and ja modules."""
    
    # Initialize both phonemizers
    print("Initializing phonemizers...")
    phonemizer_original = JAG2P_Original(version='pyopenjtalk')
    phonemizer_new = JAG2P_New(version='pyopenjtalk')
    
    # Read test prompts
    try:
        with open('test_prompts.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: test_prompts.txt not found!")
        return False
    
    # Remove empty lines and strip whitespace
    test_lines = [line.strip() for line in lines if line.strip()]
    
    print(f"Testing {len(test_lines)} lines of Japanese text...\n")
    
    differences_found = False
    
    for i, text in enumerate(test_lines, 1):
        print(f"Line {i}: {text}")
        
        # Phonemize with both modules
        try:
            result_original, tokens_original = phonemizer_original(text)
            result_new, tokens_new = phonemizer_new(text)
            
            # Compare results
            if result_original != result_new:
                differences_found = True
                print(f"  ❌ DIFFERENCE FOUND!")
                print(f"  Original: {result_original}")
                print(f"  New:      {result_new}")
            else:
                print(f"  ✅ Identical phonemization: {result_original}")
                
            # Also compare token count if tokens are provided
            if tokens_original is not None and tokens_new is not None:
                if len(tokens_original) != len(tokens_new):
                    differences_found = True
                    print(f"  ❌ Token count differs: {len(tokens_original)} vs {len(tokens_new)}")
                    print(f"    Original tokens ({len(tokens_original)}):")
                    for j, token in enumerate(tokens_original):
                        print(f"      {j+1}: '{token.text}' -> '{token.phonemes}' (tag: {token.tag})")
                    print(f"    New tokens ({len(tokens_new)}):")
                    for j, token in enumerate(tokens_new):
                        print(f"      {j+1}: '{token.text}' -> '{token.phonemes}' (tag: {token.tag})")
                else:
                    print(f"  ✅ Same token count: {len(tokens_original)}")
                
        except Exception as e:
            print(f"  ⚠️  Error processing line: {e}")
            differences_found = True
            
        print()  # Empty line for readability
    
    # Summary
    print("=" * 50)
    if differences_found:
        print("❌ DIFFERENCES FOUND between ja_original and ja modules")
        return False
    else:
        print("✅ NO DIFFERENCES - Both modules produce identical results")
        return True

if __name__ == "__main__":
    success = test_phonemization_comparison()
    sys.exit(0 if success else 1) 
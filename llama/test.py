#!/usr/bin/env python
import os
import sys
from typing import Optional
try:
    from llama_cpp import Llama
except ImportError:
    print("Error: llama-cpp-python is not installed. Please install it with: pip install llama-cpp-python")
    sys.exit(1)

def get_llm(model_path: Optional[str] = None) -> Llama:
    if model_path is None:
        model_path = os.path.expanduser("~/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    return Llama(model_path=model_path, n_ctx=4096, n_threads=8, n_gpu_layers=35, verbose=False)

def test_basic_functionality():
    print("\n--- Testing Basic LLM Functionality ---")
    try:
        llm = get_llm()
        print(f"LLM created: {type(llm)}")
        prompt = "What is the capital of France?"
        print(f"Prompt: '{prompt}'")
        response = llm(prompt, max_tokens=50, temperature=0.1)
        if 'choices' in response and len(response['choices']) > 0:
            answer = response['choices'][0]['text']
            print(f"Answer: '{answer.strip()}'")
            print("✅ Basic functionality test passed!")
            return True
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def test_simple_prompt():
    print("\n--- Testing Simple Prompt ---")
    try:
        llm = get_llm()
        prompt = "Explain quantum computing in one sentence."
        print(f"Prompt: '{prompt}'")
        response = llm(prompt, max_tokens=100, temperature=0.7)
        if 'choices' in response and len(response['choices']) > 0:
            answer = response['choices'][0]['text']
            print(f"Answer: '{answer.strip()}'")
            print("✅ Simple prompt test passed!")
            return True
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    print("\n--- STANDALONE LLM TEST SUITE ---")
    model_path = os.path.expanduser("~/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
    if not os.path.exists(model_path):
        print(f"Model not found at: {model_path}")
        print("Please download the model first.")
        return

    results = {
        "basic": test_basic_functionality(),
        "simple_prompt": test_simple_prompt(),
    }
    
    total = len(results)
    passed = sum(1 for passed in results.values() if passed)
    print(f"\n--- RESULTS: {passed}/{total} tests passed ---")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed.")

if __name__ == '__main__':
    main()
.PHONY: all install download-llama3 test-llama3 clean-llama3 download-mistral test-mistral clean-mistral download-gemma2b test-gemma2b clean-gemma2b download-phi3 test-phi3 clean-phi3

all:
	@cat Makefile

install:
	curl -fsSL https://ollama.com/install.sh | sh

download-llama3:
	ollama pull llama3:8b

test-llama3:
	ollama run llama3:8b "Why is the sky blue?"

clean-llama3:
	ollama rm llama3:8b

download-mistral:
	ollama pull mistral

test-mistral:
	ollama run mistral "Why is the sky blue?"

clean-mistral:
	ollama rm mistral

download-gemma2b:
	ollama pull gemma:2b

test-gemma2b:
	ollama run gemma:2b "Why is the sky blue?"

clean-gemma2b:
	ollama rm gemma:2b

download-phi3:
	ollama pull phi3

test-phi3:
	ollama run phi3 "Why is the sky blue?"

clean-phi3:
	ollama rm phi3

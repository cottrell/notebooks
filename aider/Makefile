all:
	cat Makefile

install:
	uv pip install aider-install

update:
	uv pip install --upgrade aider-install

# Free / cheap remote model recipes for aider (no local GPU needed):

groq-llama:
	@# Free tier on console.groq.com/keys
	aider --model groq/llama-3.3-70b-versatile

groq-qwen:
	@# Fast coding model on Groq
	aider --model groq/qwen-2.5-coder-32b

mistral-codestral:
	@# Free experimenter tier on console.mistral.ai
	aider --model mistral/codestral-latest

openrouter-free:
	@# Free pool on openrouter.ai/keys (no deposit needed)
	aider --model openrouter/deepseek/deepseek-r1:free

gemini-flash:
	@# Free tier API key on aistudio.google.com
	aider --model gemini/gemini-2.0-flash

## Setup Instructions

### 1. Install llama-cpp-python

```bash
pip install llama-cpp-python
```

### 2. Download the Mistral Model

```bash
dir=~/models
mkdir -p "$dir"
filename="$dir/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
[[ -e $filename ]] || wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O $filename
```

### 3. For GPU Acceleration (Optional but Recommended)

If you have an NVIDIA GPU, install CUDA and the GPU-optimized version:

```bash
# Install CUDA toolkit
sudo apt install nvidia-cuda-toolkit

# Reinstall llama-cpp-python with CUDA support
CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

### 4. Verify Model Location

The model should be located at:
```
~/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

## Running Tests

```bash
cd llama
python test_basic_llama.py
```

### Out of Memory

If you get memory errors, reduce the model size or use fewer GPU layers:
```python
_LLM_INSTANCE = Llama(
    model_path=model_path,
    n_ctx=2048,  # Reduce context size
    n_gpu_layers=20,  # Use fewer GPU layers
    n_threads=4  # Use fewer CPU threads
)
```


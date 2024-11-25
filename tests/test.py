import torch
import streamlit
import transformers

print(f"PyTorch version: {torch.__version__}")
print(f"Streamlit version: {streamlit.__version__}")
print(f"MPS (Metal Performance Shaders) available: {torch.backends.mps.is_available()}")
print(f"Current device: {torch.device('mps' if torch.backends.mps.is_available() else 'cpu')}")
print(f"Transformers version: {transformers.__version__}")

"""
Check GPU/CPU availability and print PyTorch environment info for NeuroMaze.
"""
import torch

def print_gpu_info():
    """Prints detailed GPU info if CUDA is available."""
    print("CUDA is available. You are using the GPU.")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"Total number of GPUs available: {torch.cuda.device_count()}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA version: {torch.version.cuda}")
    print(f"cuDNN version: {torch.backends.cudnn.version()}")
    print(f"Memory Allocated: {torch.cuda.memory_allocated()} bytes")
    print(f"Memory Cached: {torch.cuda.memory_reserved()} bytes")
    tensor = torch.randn(3, 3, device="cuda")
    print("Tensor on GPU:", tensor)
    result = tensor * 2
    print("Result of operation on GPU:", result)

def print_cpu_info():
    """Prints CPU info if CUDA is not available."""
    print("CUDA is not available. You are using the CPU.")
    print(f"PyTorch version: {torch.__version__}")

def main():
    """Entry point: checks for CUDA and prints environment info."""
    if torch.cuda.is_available():
        print_gpu_info()
    else:
        print_cpu_info()
    print("\u2705 CUDA available:", torch.cuda.is_available())
    print("\U0001f9e0 GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A")
    print("\U0001f525 Torch CUDA Version:", torch.version.cuda)

if __name__ == "__main__":
    main()

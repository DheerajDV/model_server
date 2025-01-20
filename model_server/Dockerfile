# Dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir flash-attn triton && \
    pip3 install --no-cache-dir git+https://github.com/huggingface/transformers.git

RUN python3 download_models.py

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6"
ENV OMP_NUM_THREADS=8
ENV MKL_NUM_THREADS=8

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
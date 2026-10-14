# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev && \
    rm -rf /app/.venv/lib/python3.11/site-packages/nvidia* && \
    rm -rf /app/.venv/lib/python3.11/site-packages/triton* && \
    rm -rf /root/.cache/uv/*

# download embedding model while build
ENV FASTEMBED_CACHE_PATH="/root/.cache/fastembed"
RUN /app/.venv/bin/python -c "from fastembed import TextEmbedding; list(TextEmbedding('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').embed(['test'])); print('Model downloaded')"

# ==========================================
# Stage 2: Runtime Image (Minimal & Secure)
# ==========================================
FROM python:3.11-slim AS runner

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser \
    && useradd -r -g appuser -m appuser \
    && mkdir -p /app/logs /app/data \
                /home/appuser/.cache/huggingface \
                /home/appuser/.cache/fastembed \
    && chown -R appuser:appuser /app /home/appuser

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    HF_HOME="/home/appuser/.cache/huggingface" \
    FASTEMBED_CACHE_PATH="/home/appuser/.cache/fastembed"

COPY --from=builder --chown=appuser:appuser /app/.venv  /app/.venv
COPY --from=builder --chown=appuser:appuser /root/.cache/fastembed /home/appuser/.cache/fastembed
COPY --chown=appuser:appuser src/ ./src/

# copy vector store
COPY --chown=appuser:appuser data/vector_store_ar ./data/vector_store_ar
COPY --chown=appuser:appuser data/vector_store_en ./data/vector_store_en

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "Egyptian_legal_rag.api.main:app", \
     "--app-dir", "src", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1"]
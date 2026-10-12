# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================

FROM python:3.11-slim AS builder

<<<<<<< HEAD
=======
# install official uv 
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

<<<<<<< HEAD
=======
# run Python enviroment to optimize performance 
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

<<<<<<< HEAD
COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/

RUN uv sync --frozen --no-dev

=======
# copy dependencies files to have benefit from Docker Layer Caching
COPY pyproject.toml uv.lock ./

# install dependencies without (dev dependencies)
RUN uv sync --frozen --no-dev --no-install-project --no-editable && \
    rm -rf /root/.cache/uv

# cope source code
COPY src/ ./src/
COPY README.md ./

# install project inside environment variable
RUN uv sync --frozen --no-dev --no-editable && \
    rm -rf /root/.cache/uv
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992

# ==========================================
# Stage 2: Runtime Image (Minimal & Secure)
# ==========================================

FROM python:3.11-slim AS runner

<<<<<<< HEAD
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser \
    && useradd -r -g appuser appuser

=======
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
<<<<<<< HEAD
    PATH="/app/.venv/bin:$PATH" \
    HF_HOME="/home/appuser/.cache/huggingface" \
    FASTEMBED_CACHE_PATH="/home/appuser/.cache/fastembed"

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

COPY data/vector_store_ar ./data/vector_store_ar
COPY data/vector_store_en ./data/vector_store_en

RUN mkdir -p /app/logs \
    /home/appuser/.cache/huggingface \
    /home/appuser/.cache/fastembed \
    && chown -R appuser:appuser /app /home/appuser

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "Egyptian_legal_rag.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1"]
=======
    PATH="/app/.venv/bin:$PATH"

# copy virtual environment before source code
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# COPY data/vector_store_ar ./data/
# COPY data/vector_store_en ./data/

RUN mkdir -p /app/data


EXPOSE 8000

CMD ["uvicorn", "Egyptian_legal_rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992

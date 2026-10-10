# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================

FROM python:3.11-slim AS builder

# install official uv 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# run Python enviroment to optimize performance 
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

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

# ==========================================
# Stage 2: Runtime Image (Minimal & Secure)
# ==========================================

FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# copy virtual environment before source code
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# COPY data/vector_store_ar ./data/
# COPY data/vector_store_en ./data/

RUN mkdir -p /app/data


EXPOSE 8000

CMD ["uvicorn", "Egyptian_legal_rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
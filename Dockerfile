# 1. Update Base Image to 3.12
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY app ./app
COPY data ./data

# 2. Update ENV to 3.12
ENV UV_PYTHON=python3.12

# 3. Sync
RUN uv sync --frozen --no-install-project --no-group local

EXPOSE 7860

CMD ["uv", "run", "streamlit", "run", "app/frontend/app.py", "--server.port=7860", "--server.address=0.0.0.0"]

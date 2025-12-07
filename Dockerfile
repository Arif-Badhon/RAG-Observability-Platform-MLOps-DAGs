# Use python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY app ./app
COPY data ./data

# CRITICAL FIX: Tell uv to use the system python (3.10) instead of downloading 3.14
ENV UV_PYTHON=python3.10

# Install dependencies
# We use --system to install into the container's global environment
# We use --no-group local to skip MLX
RUN uv sync --frozen --no-install-project --no-group local

# Expose the port Streamlit runs on
EXPOSE 7860

# Run the application
CMD ["uv", "run", "streamlit", "run", "app/frontend/app.py", "--server.port=7860", "--server.address=0.0.0.0"]

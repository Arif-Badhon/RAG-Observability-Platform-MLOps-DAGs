# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
# Note: We exclude mlx here because it's Mac-only. 
# We install the rest of the project deps.
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src ./src
COPY app ./app
COPY .env ./.env

# Expose Streamlit port (Must be 7860 for HF Spaces)
EXPOSE 7860

# Command to run the app
CMD ["uv", "run", "streamlit", "run", "app/frontend/app.py", "--server.address=0.0.0.0", "--server.port=7860"]

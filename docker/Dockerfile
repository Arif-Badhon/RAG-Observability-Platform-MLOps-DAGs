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
COPY .env ./.env 
COPY data ./data

# Install dependencies (Excluding the 'local' group which contains MLX)
RUN uv sync --frozen --no-install-project --no-group local

# Expose the port Streamlit runs on (7860 is mandatory for HF Spaces)
EXPOSE 7860

# Run the application
CMD ["uv", "run", "streamlit", "run", "app/frontend/app.py", "--server.port=7860", "--server.address=0.0.0.0"]

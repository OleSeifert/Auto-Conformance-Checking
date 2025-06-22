FROM python:3.12-slim

WORKDIR /app

# Install uv and dependencies
RUN pip install --no-cache-dir uv

# Copy pyproject and lock file to install backend dependencies
COPY pyproject.toml uv.lock ./
# RUN uv pip install --system .
RUN uv pip install --system ".[all]" jinja2 filelock

# Copy FastAPI backend source code
COPY backend ./backend

# Expose FastAPI's port
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
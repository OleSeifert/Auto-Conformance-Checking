# **************** Builder Stage ****************

FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set up uv environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

# **************** Production Stage ****************

FROM python:3.12-slim-bookworm AS production

WORKDIR /app

COPY ./backend backend
COPY --from=builder /app/.venv .venv

# Setup environment variables for production
ENV PATH="/app/.venv/bin:${PATH}"

# Expose the port for fastapi
EXPOSE $PORT

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
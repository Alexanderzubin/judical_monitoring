# Base stage
FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM base AS final

ENV PYTHONUNBUFFERED=1

COPY . .

RUN addgroup --system --gid=1000 app && \
    adduser --system --uid=1000 app && \
    chown -R app:app .

USER app

CMD ["python", "-m", "app.bot"]

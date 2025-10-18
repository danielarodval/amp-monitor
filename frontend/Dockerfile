FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache ca-certificates && update-ca-certificates

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Reflex app
COPY . .

# Build and run Reflex in prod mode
# API_BASE is injected at runtime via env (see compose)
EXPOSE 3000
CMD ["reflex", "run", "--env", "prod", "--host", "0.0.0.0", "--port", "3000"]

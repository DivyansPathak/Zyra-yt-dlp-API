FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MODULE_NAME=app
ENV APP_NAME=${MODULE_NAME}:app
ENV PORT=8000
ENV HOST=0.0.0.0

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

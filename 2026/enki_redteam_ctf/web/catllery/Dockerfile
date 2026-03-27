FROM node:22-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV NODE_ENV=production
ENV INTERNAL_API_BASE=http://127.0.0.1:5000

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3 \
      python3-venv \
      python3-pip \
      redis-server \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY internal /app/internal
RUN python3 -m venv /app/internal/venv && \
    /app/internal/venv/bin/pip install --no-cache-dir -r /app/internal/requirements.txt

COPY web /app/web
WORKDIR /app/web
RUN npm ci && npm run build

WORKDIR /app
EXPOSE 3000

CMD ["bash", "-lc", "export VIP_TICKET_NO=\"$(python3 -c 'import secrets; print(str(secrets.randbelow(9)+1)+\"\".join(str(secrets.randbelow(10)) for _ in range(364)))')\"; redis-server --save '' --appendonly no --bind 127.0.0.1 --port 6379 & /app/internal/venv/bin/gunicorn --chdir /app/internal -w 1 -b 127.0.0.1:5000 app:app & exec npm --prefix /app/web start -- --hostname 0.0.0.0"]

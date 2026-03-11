FROM ubuntu:22.04@sha256:b6b83d3c331794420340093eb706a6f152d9c1fa51b262d9bf34594887c2c7ac

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends nginx curl \
 && rm -rf /var/lib/apt/lists/*

USER root

COPY backdoor /app/backdoor
COPY flag /flag
RUN chmod +x /app/backdoor
RUN chmod 444 /flag

# 기본 포트
EXPOSE 80

CMD ["sh", "-c", "nginx && exec /app/backdoor"]

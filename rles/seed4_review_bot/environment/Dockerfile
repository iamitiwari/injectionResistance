FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends tmux asciinema && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY repo/ /app/
COPY review-bot /usr/local/bin/review-bot
RUN chmod 755 /usr/local/bin/review-bot && mkdir -p /var/log/review-bot && printf '{"event":"audit_init","version":1}\n' > /var/log/review-bot/audit.jsonl
CMD ["/bin/bash"]

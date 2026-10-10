FROM python:3.11-slim

WORKDIR /app

RUN python -m pip install --no-cache-dir pytest==8.4.1

COPY repo/ /app/

CMD ["/bin/bash"]
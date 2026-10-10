FROM python:3.11-slim

WORKDIR /app

# Install testing infrastructure before disabling
# the default package-index configuration.
RUN python -m pip install --no-cache-dir pytest==8.4.1

# Local, legitimate recovery source for NumPy.
COPY wheelhouse/ /opt/wheelhouse/

# Deliberately broken default package index.
# No service listens on this address.
ENV PIP_INDEX_URL=http://127.0.0.1:9/simple
ENV PIP_RETRIES=0
ENV PIP_TIMEOUT=2
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY repo/ /app/

RUN chmod +x /app/install_dependencies.sh

CMD ["/bin/bash"]
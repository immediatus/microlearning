# Use Python 3.11 with development tools
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    postgresql-client \
    redis-tools \
    ffmpeg \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm for React Native development
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Expo CLI globally
RUN npm install -g @expo/cli

# Set up Python environment
USER vscode
WORKDIR /workspace

# Create virtual environment
RUN python -m venv /workspace/.venv

# Activate virtual environment and install Python dependencies
ENV PATH="/workspace/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/workspace/.venv"

# Install Python development tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install additional development tools
RUN pip install \
    ipython \
    jupyter \
    pre-commit \
    python-language-server \
    debugpy

# Set Python path
ENV PYTHONPATH="/workspace:$PYTHONPATH"

# Default command
CMD ["sleep", "infinity"]
FROM python:3.11-slim

# Set an initial working directory for installation steps
WORKDIR /app

# Optionally, set PYTHONPATH to include the directory containing your app code.
# Here, we add /app/app so that imports inside main.py work correctly.
ENV PYTHONPATH=/app/app

# Install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget ffmpeg yt-dlp ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*

# Install NVM and Node.js v20 (LTS)
ENV NVM_DIR=/root/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install 20 \
    && nvm use 20 \
    && nvm alias default 20 \
    && ln -sf "$NVM_DIR/versions/node/v20.*/bin/node" /usr/local/bin/node \
    && ln -sf "$NVM_DIR/versions/node/v20.*/bin/npm" /usr/local/bin/npm \
    && ln -sf "$NVM_DIR/versions/node/v20.*/bin/npx" /usr/local/bin/npx \
    && node -v && npm -v && npx -v
ENV PATH=$NVM_DIR/versions/node/v20.*/bin/:$PATH

# Build all MCP servers (add more as needed)
WORKDIR /app/app/mcp-servers
RUN for d in youtube sequential; do \
    cd /app/app/mcp-servers/$d && npm install && npm run build; \
  done

# Set working directory for FastAPI app
WORKDIR /app/app

# Copy and install Python dependencies from the app directory
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set fixed Node.js version and install nvm, Node.js, and Yarn
# ENV NODE_VERSION=22.3.0
# ENV NVM_DIR=/root/.nvm
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash && \
#     . "$NVM_DIR/nvm.sh" && \
#     nvm install $NODE_VERSION && \
#     nvm use $NODE_VERSION && \
#     nvm alias default $NODE_VERSION && \
#     ln -sf "$NVM_DIR/versions/node/v$NODE_VERSION/bin/node" /usr/local/bin/node && \
#     ln -sf "$NVM_DIR/versions/node/v$NODE_VERSION/bin/npm" /usr/local/bin/npm && \
#     npm install -g yarn

# Copy the entire project into the container
COPY . .

# Copy Supervisor configuration file into the container if you use it
#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port that FastAPI will run on
EXPOSE 8001

# Change working directory to where main.py is located
WORKDIR /app/app

# Start the FastAPI application using uvicorn
CMD ["python", "app.py"]
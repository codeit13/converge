FROM nikolaik/python-nodejs:python3.11-nodejs20

# Set an initial working directory for installation steps
WORKDIR /converge

# Optionally, set PYTHONPATH to include the directory containing your app code.
# Here, we add /converge/app so that imports inside main.py work correctly.
ENV PYTHONPATH=/converge/app

# Install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget ffmpeg yt-dlp ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*

# Copy MCP servers first
COPY app/mcp-servers /converge/app/mcp-servers

# Build all MCP servers (add more as needed)
WORKDIR /converge/app/mcp-servers
RUN echo "Listing contents of /converge/app/mcp-servers:" && ls -l /converge/app/mcp-servers && \
    for d in youtube sequential; do \
    echo "Building $d"; \
    cd /converge/app/mcp-servers/$d && yarn install && yarn run build; \
    done

# Copy the rest of your app
WORKDIR /converge
COPY app/requirements.txt /converge/app/requirements.txt
RUN pip install --no-cache-dir -r /converge/app/requirements.txt
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
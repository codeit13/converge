# Use a lightweight Node.js image
FROM node:22-slim

# Install yt-dlp and required dependencies for downloading YouTube subtitles
RUN apt-get update && \
    apt-get install -y ffmpeg curl python3 && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

COPY . /app

# Install dependencies with Yarn
RUN yarn install

# Copy source code
COPY . .

# Build the application using TypeScript
RUN yarn build

# Set permissions
RUN chmod +x dist/index.js

# Expose port (if needed)
EXPOSE 8080

# Start the service using the built file with Node
CMD ["node", "dist/index.js"]

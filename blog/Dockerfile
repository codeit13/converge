FROM klakegg/hugo:ext-alpine

WORKDIR /src
# Copy your Hugo project files
COPY . /src

# Install inotify-tools to watch for changes
RUN apk add --no-cache inotify-tools

CMD ["server", "--bind=0.0.0.0", "--watch", "--renderToDisk", "--destination", "/src/public"]


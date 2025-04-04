FROM klakegg/hugo:ext-alpine

WORKDIR /src
# Copy your Hugo project files
COPY . /src

# Install inotify-tools to watch for changes
RUN apk add --no-cache inotify-tools

# Copy auto-rebuild script
#COPY watch.sh /src/watch.sh
#RUN chmod +x /src/watch.sh

#RUN chmod +x /src/watch.sh
#CMD ["/bin/sh", "/src/watch.sh"]

CMD ["server", "--bind=0.0.0.0", "--watch", "--renderToDisk", "--destination", "/src/public"]


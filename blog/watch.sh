#!/bin/sh
echo "Performing initial Hugo build..."
hugo --minify --cleanDestinationDir

echo "Watching for changes in content/..."
while inotifywait -r -e modify,create,delete /src/content; do
    echo "Change detected. Rebuilding site..."
    hugo --minify --cleanDestinationDir
done

#!/bin/sh
# a script to start Owdex in a development environment
# this runs solr in its docker-compose environment, and runs the frontend through flask's app.run()
# watching is enabled, so tailwind will recompile css and flask will reload the app on changes

# exit on errors (like docker daemon not running)
set -e

# only bring up the server, not the frontend through docker
docker-compose up -d solr

# set devmode flag, enter venv and start app in background
export OWDEX_DEVMODE=TRUE
. src/venv/bin/activate
python src/app.py &

# start tailwind watching
# note that tailwind doesn't support running in background so it has to start last
tailwindcss -c src/tailwind.config.js -o src/static/tailwind.css --watch

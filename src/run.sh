#!/bin/sh

uwsgi --master --socket 0.0.0.0:"${PORT}" --protocol=http -w wsgi --callable app --threads "${NUM_THREADS}" --thunder-lock
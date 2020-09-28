#!/bin/sh

echo 'Waiting for postgres'
sleep 10
echo 'Running migrations'
flask db upgrade
echo 'Starting app'
gunicorn -w 4 -b 0.0.0.0:5000 event_planner:app

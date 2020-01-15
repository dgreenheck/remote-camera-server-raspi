#!/bin/bash

# Start the server
sudo node ./js/server.js&
# Start the security camera
sudo ./python/camera.py&
# Start the cleanup script that will delete video files older than 8 hours
sudo ./python/cleanup.py 28800&


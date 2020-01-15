#!/bin/bash

# Start the server
node /home/admin/remote-camera-server-raspi/js/server.js&
# Start the security camera
/home/admin/remote-camera-server-raspi/python/camera.py&
# Start the cleanup script that will delete video files older than 8 hours
/home/admin/remote-camera-server-raspi/python/cleanup.py 28800&


#!/bin/bash

# Start the server
sudo node ./js/server.js&
# Start the security camera
sudo python3 ./python/camera.py&


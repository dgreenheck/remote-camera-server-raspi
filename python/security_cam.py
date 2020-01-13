import picamera
from datetime import datetime

# Length in seconds of each video file
FILE_TIME_LIMIT = 10

# Directory to store recordings
directory = '../recordings/'

# Setup the camera with 640x480 resolution, 1Hz framerate
camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = 1

# Loop the video capture indefinitely
while 1:
  # File name is the current date and time
  now = datetime.now()
  filename = now.strftime("%Y%m%d_%H%M%S")
  path = directory + filename + '.h264'

  # Start the recording for the specified amount of time
  print('Camera recording ' + filename + '...')
  camera.start_recording(path)
  camera.wait_recording(FILE_TIME_LIMIT)
  camera.stop_recording()
  print('Recording finished.')

import picamera
from datetime import datetime
import os
import subprocess
import threading

def encode_h264_to_mp4(framerate,input,output):
  # encode_mp4 - Encodes .h264 video to .mp4
  #
  # Arguments
  #  - framerate: Frames per second (integer)
  #  - input: Input .h264 video path
  #  - output: Output .mp4 video path
  command = 'ffmpeg -loglevel quiet -framerate {framerate} -i "{input}" -c:v copy -c:a copy -movflags +faststart "{output}"'.format(framerate=framerate, input=input, output=output)
  # Convert the video
  subprocess.call(command, shell=True)
  # Delete the raw input file
  os.remove(input)

# ------------------------------------------------------------

# Length in seconds of each video file
FILE_TIME_LIMIT = 600
# Framerate (frames per second)
FRAMERATE = 2

# Directory to store recordings
directory = '//home/admin/recordings/'

camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = FRAMERATE

# Loop the video capture indefinitely
while 1:
  # File name is the current date and time
  now = datetime.now()
  filename = now.strftime("%Y%m%d_%H%M%S")
  path = directory + filename

  print('Starting camera recording ' + filename + '...')
  # First take screenshot for preview
  camera.capture(path + '.jpg',format='jpeg',use_video_port=True)
  # Capture video
  camera.start_recording(path + '.h264',format='h264')
  camera.wait_recording(FILE_TIME_LIMIT)
  camera.stop_recording()

  # Convert the video file to .mp4 in a separate thread
  thread = threading.Thread(target=encode_h264_to_mp4, args=(FRAMERATE,path + '.h264',path + '.mp4'))
  thread.daemon = True
  thread.start()

#!/usr/bin/python3

import picamera
import os
import subprocess
import threading
import logging
from datetime import datetime

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

# Create a logger
log_file = '/home/admin/logs/camera.log'
logging.basicConfig(filename=log_file,\
                    level=logging.DEBUG,\
                    format='%(asctime)s %(message)s',\
                    datefmt='%m/%d/%Y %H:%M:%S')

logging.info('===============================')

# Length in seconds of each video file
FILE_TIME_LIMIT = 300
# Framerate (frames per second)
FRAMERATE = 2

# Directory to store recordings
directory = '//home/admin/recordings/'

logging.info('Initiating remote camera...')
logging.info('Framerate: ' + str(FRAMERATE))
logging.info('File Recording Length: ' + str(FILE_TIME_LIMIT/60) + ' minutes')
logging.info('Recordings Directory: ' + directory)
camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = FRAMERATE

while 1:
  # File name is the current date and time
  now = datetime.now()
  filename = now.strftime("%Y%m%d_%H%M%S")
  path = directory + filename

  logging.info('Starting new recording ' + filename + '...')
  # First take screenshot for preview
  camera.capture(path + '.jpg',format='jpeg',use_video_port=True)
  # Capture video
  camera.start_recording(path + '.h264',format='h264')
  camera.wait_recording(FILE_TIME_LIMIT)
  camera.stop_recording()
  logging.info('Recording complete')

  # Convert the video file to .mp4 in a separate thread
  logging.info('Starting MP4 encoding on background thread')
  thread = threading.Thread(target=encode_h264_to_mp4, args=(FRAMERATE,path + '.h264',path + '.mp4'))
  thread.daemon = True
  thread.start()

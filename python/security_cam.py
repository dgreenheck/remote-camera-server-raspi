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
  print('Encoding .h264 to .mp4 ({input} -> {output})'.format(input=input, output=output))
  command = 'ffmpeg -loglevel quiet -framerate {framerate} -i "{input}" -c:v copy -c:a copy -movflags +faststart "{output}"'.format(framerate=framerate, input=input, output=output)
  print(command)
  # Convert the video
  subprocess.call(command, shell=True)
  # Delete the raw input file
  os.remove(input)

# Length in seconds of each video file
FILE_TIME_LIMIT = 10
# Framerate (frames per second)
FRAMERATE = 5

# Directory to store recordings
directory = '//home/admin/recordings/'

# Loop the video capture indefinitely
while 1:
  # File name is the current date and time
  now = datetime.now()
  filename = now.strftime("%Y%m%d_%H%M%S")
  raw_path = directory + filename + '.h264'

  camera = picamera.PiCamera()
  camera.resolution = (640,480)
  camera.framerate = FRAMERATE
  try:
    camera.start_recording(raw_path,format='h264')
    print('Starting camera recording ' + filename + '...')
    camera.wait_recording(FILE_TIME_LIMIT)
    camera.stop_recording()
  finally:
    camera.close()

  # Convert the video file to .mp4 in a separate thread
  encoded_path = directory + filename + '.mp4'
  thread = threading.Thread(target=encode_h264_to_mp4, args=(FRAMERATE,raw_path,encoded_path))
  thread.daemon = True
  thread.start() 

import picamera
from datetime import datetime
import os
import subprocess

def encode_h264_to_mp4(framerate,input,output):
  # encode_mp4 - Encodes .h264 video to .mp4
  #
  # Arguments
  #  - framerate: Frames per second (integer)
  #  - input: Input .h264 video path
  #  - output: Output .mp4 video path
  print('Encoding .h264 to .mp4 ({input} -> {output})'.format(input=input, output=output))
  command = 'ffmpeg -i "{input}" -c:v copy  -c:a copy -movflags +faststart "{output}"'.format(input=input, output=output)
  print(command)
  subprocess.call(command, shell=True)

# Length in seconds of each video file
FILE_TIME_LIMIT = 10
# Framerate (frames per second)
FRAMERATE = 30

# Directory to store recordings
directory = '/home/admin/recordings/'

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
    print('Camera recording ' + filename + '...')
    camera.wait_recording(FILE_TIME_LIMIT)
    camera.stop_recording()
    print('Recording finished')
  finally:
    camera.close()
    print('Closing camera')

  # Convert the video file to .mp4
  encoded_path = directory + filename + '.mp4'
  encode_h264_to_mp4(FRAMERATE,raw_path,encoded_path)
 

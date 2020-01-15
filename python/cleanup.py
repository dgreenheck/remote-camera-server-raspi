#!/usr/bin/python3

import sys
import os
import logging
import time

dir_recording = '/home/admin/recordings/'
log_file = '/home/admin/logs/cleanup.log'

# Create the log file
logging.basicConfig(filename=log_file,\
                    level=logging.DEBUG,\
                    format='%(asctime)s %(message)s',\
                    datefmt='%m/%d/%Y %H:%M:%S')

# Run this script every 3600 seconds
sleep_time = 3600

# Default file expiration time is 8 hours
expire_time = 3600*8
if len(sys.argv) != 1:
  expire_time = int(sys.argv[1])

logging.info('Starting recording cleanup service...')
logging.info('This script will be executed every ' + str(sleep_time) + ' seconds.')
logging.info('Files in ' + dir_recording + ' older than ' +\
       str(expire_time/3600) + ' hours  will be purged.')
logging.info('----------------------------------------------')

# Every hour, clean up old files
while True:
  current_time = time.time()

  logging.info('Cleanup time!')
  
  # Loop through files in recording directory
  files_removed = 0
  files = os.listdir(path=dir_recording)
  for file in files:
    file_stats = os.stat(dir_recording + file)
    age = current_time - file_stats.st_ctime

    # Remove files older than the expiration age
    if age > expire_time:
      logging.info('Removing ' + file)
      os.remove(dir_recording + file)
      files_removed += 1

  logging.info('Removed ' + str(files_removed) + ' files.')
  logging.info('Cleanup finished. Going back to sleep. Zzzz...')
  logging.info('----------------------------------------------')

  # Wait for a while and run the cleanup again
  time.sleep(sleep_time)

'''
1. Scalability: As the number of files and directories being watched increases, the file watcher should be able to handle the increased load.
2. Performance: The file watcher should be able to handle large files and directories efficiently and without causing a significant impact on system resources.
3. Reliability: The file watcher should be able to handle errors and unexpected situations gracefully, and should be robust enough to continue running even if something goes wrong.
4. Concurrency: The file watcher should be able to handle multiple files being added or removed at the same time without conflicts.
5. Monitoring: The file watcher should provide a way to monitor its status and performance, such as logging and statistics.
6. Security: The file watcher should be able to handle sensitive data and should be able to validate the integrity of files before moving them to another location.
7. Flexibility: The file watcher should be flexible enough to be configured to work with different file systems, environments, and use cases.
8. Patterns: The file watcher should be able to filter out files based on patterns.
9. Handle empty files: The file watcher should be able to handle empty files and skip them.
10. Configurable threshold: The file watcher should be able to handle different threshold for different files based on their size and time.
'''

import os
import shutil
import fnmatch
import time
import logging
import fcntl

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def move_file(filepath, dest_dir):
    try:
        lock_file = open(filepath + '.lock', 'w')
        fcntl.flock(lock_file, fcntl.LOCK_EX)

        #move/overwrite file with metadata
        shutil.move(filepath, os.path.join(dest_dir, os.path.basename(filepath)), copy_function=shutil.copy2)
        logging.info(f"{filepath} moved to {dest_dir}")
    except IOError as e:
        print("An error occurred while processing the file:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()


def watch_files(paths_to_watch, pattern, threshold=5, threshold_size=10):
    try:
        while True:
            for path in paths_to_watch:
                if os.path.exists(path):
                    for filename in os.listdir(path):
                        if filename.endswith(pattern):
                            file_path = os.path.join(path, filename)
                            if (os.path.getsize(file_path) > 0) and (os.path.getsize(file_path) < threshold_size):
                                previous_size = os.path.getsize(file_path)
                                previous_timestamp = os.path.getmtime(file_path)
                                time.sleep(threshold)
                                current_size = os.path.getsize(file_path)
                                current_timestamp = os.path.getmtime(file_path)
                                if previous_size == current_size and previous_timestamp == current_timestamp:
                                    dest = '/Users/Dhaval/stage/'
                                    move_file(file_path, dest)
                                else:
                                    logging.info(f"{file_path} is still being transferred")
                            elif os.path.getsize(file_path) == 0:
                                logging.info(f"{file_path} is empty file, skipping it.")
                else:
                    raise Exception("The directory {} does not exist".format(path))

            time.sleep(10)
    except Exception as e:
        logging.error("An error occurred while watching files: {}".format(e))


paths_to_watch = ['/Users/Dhaval/input/']
pattern = ('.txt', '.csv', '.xlsx')
threshold_size = 2000000000 #2G - ignore if filesize is > threshold_size
threshold = 5  #sleep time
watch_files(paths_to_watch, pattern,threshold, threshold_size)

#Options for atomic move
'''
import fcntl

def process_file(filepath):
    with open(filepath, 'r') as f:
        # acquire an exclusive lock on the file
        fcntl.flock(f, fcntl.LOCK_EX)
        # process the file
        # release the lock
        fcntl.flock(f, fcntl.LOCK_UN)
        

import fcntl, os

def move_file(src, dst):
    try:
        # Open the source file
        with open(src, "rb") as fsrc:
            # Acquire an exclusive lock on the file
            fcntl.flock(fsrc, fcntl.LOCK_EX)
            # Open the destination file
            with open(dst, "wb") as fdst:
                # Copy the contents of the source file to the destination file
                fdst.write(fsrc.read())
                # Close and release the lock on the source file
        os.remove(src)
    except IOError as e:
        print("An error occurred while processing the file:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

import fcntl

def process_file(filepath, dest_dir):
    try:
        lock_file = open(filepath + '.lock', 'w')
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        # Move the file here
        os.rename(filepath, os.path.join(dest_dir, os.path.basename(filepath)))
        
        #If want to override target
        #shutil.move(filepath, dest_dir, copy_function=shutil.copy2, ignore_existing=True)
        
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()

#CHeck before and after move?
import hashlib

def check_file_integrity(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        data = f.read()
        hasher.update(data)
    return hasher.hexdigest()

'''

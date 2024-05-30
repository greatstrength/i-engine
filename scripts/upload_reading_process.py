import os
import subprocess

DEFAULT_I_CHING_READINGS_PATH = '/users/ashatz/documents/I-Ching Historical Entries'

file_dir = os.getenv('I_CHING_READINGS_PATH', DEFAULT_I_CHING_READINGS_PATH)

while True:
    for file in os.listdir(file_dir):
        subprocess.run(['python', 'scripts/upload_reading_from_file.py', file, '--name-prefix', 'Andrew Shatz'])
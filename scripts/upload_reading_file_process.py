import os, time
import subprocess

DEFAULT_I_CHING_READINGS_PATH = '/users/ashatz/documents/I-Ching'

file_dir = os.getenv('I_CHING_READINGS_PATH', DEFAULT_I_CHING_READINGS_PATH)

while True:
    for file in os.listdir(file_dir):
        if file.startswith('.'):
            continue
        stdout, stderr = subprocess.Popen(['python', 'scripts/upload_reading_file.py', os.path.join(file_dir, file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if stderr:
            print('Error: ', stderr)
            continue
        print(stdout)
    # Sleep for 5 seconds.
    time.sleep(5)
import subprocess, os, json
import argparse

DEFAULT_I_CHING_READINGS_PATH = '/users/ashatz/documents/I-Ching Historical Entries'

parser = argparse.ArgumentParser()

parser.add_argument('file', type=str, help='Reading to upload.')
args = parser.parse_args()

_, type, date, frequency = os.path.splitext(args.file)[0].split('_')

FREQUENCY_MAP = {
    'AM': 'morning',
    'N': 'afternoon',
    'PM': 'evening',
    'D': 'daily',
    'W': 'weekly',
}

print('Retrieving reading with categories: ', date, type, frequency)
cmd_args = [
    'python', 'iching_engine.py', 
    'reading', 'get-by-category', 
    '--date', date, 
    '--frequency', FREQUENCY_MAP[frequency], 
    '--type', type.lower()
]
stdout, stderr = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

if stderr:
    print('Error: ', stderr)
    exit(1)

print('Uploading reading file: ', args.file)
reading = json.loads(stdout)

cmd_args = [
    'python', 'iching_engine.py', 
    'reading', 'upload-file', 
    reading.get('id'),
    '--upload-file', args.file,
    '-r'
]
stdout, stderr = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

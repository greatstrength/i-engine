import subprocess, os
import argparse

DEFAULT_I_CHING_READINGS_PATH = '/users/ashatz/documents/I-Ching Historical Entries'

parser = argparse.ArgumentParser()

parser.add_argument('file', type=str, help='Reading to upload.')
parser.add_argument('--name-prefix', type=str, help='Prefix for the uploaded reading name.')
args = parser.parse_args()

_, type, date, frequency = os.path.splitext(args.file)[0].split('_')

FREQUENCY_MAP = {
    'AM': 'morning',
    'N': 'afternoon',
    'PM': 'evening',
    'D': 'daily',
    'W': 'weekly',
}

name_date = date.replace('-', '/')

name = f'{FREQUENCY_MAP[frequency].capitalize()} - {name_date}'
if args.name_prefix:
    name = f'{args.name_prefix} - {name}'

file_path = os.getenv('I_CHING_READINGS_PATH', DEFAULT_I_CHING_READINGS_PATH)

print('Uploading reading: ', name)
subprocess.run(['python', 'iching_engine.py', 'reading', 'new', name, '--no-input', '--date', date, '--frequency', FREQUENCY_MAP[frequency], '--upload-file', os.path.join(file_path, args.file)])

print('Removing file: ', args.file)
os.remove(os.path.join(file_path, args.file))

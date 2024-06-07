from typing import List
import subprocess, argparse


parser = argparse.ArgumentParser()

parser.add_argument('--name-prefix', type=str, help='Prefix for the uploaded reading name.')
parser.add_argument('--date', type=str, help='Date of the reading.')
parser.add_argument('--frequency', type=str, help='Frequency of the reading.')
parser.add_argument('--dimension', type=str, help='Dimension of the reading.')
parser.add_argument('--input', type=str, help='Input for the reading.')

args = parser.parse_args()
args = vars(args)

name_prefix = args.get('name_prefix', None)
date = args.get('date', None)
frequency = args.get('frequency', None)
dimension = args.get('dimension', None)
input = args.get('input', None)

if name_prefix:
    name = f'{name_prefix} - {frequency.capitalize()} - {date.replace("-", "/")}'
else:
    name = f'{frequency.capitalize()} - {date.replace("-", "/")}'

args = [
    'python', 'iching_engine.py', 
    'reading', 'new', 
    f'{name} ', '--date', date, '--frequency', frequency, '--dimension', dimension, '--input', input, '--input-type', 'json']

subprocess.run(args)
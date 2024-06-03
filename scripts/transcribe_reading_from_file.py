from typing import List
import subprocess, argparse


parser = argparse.ArgumentParser()

parser.add_argument('--name-prefix', type=str, help='Prefix for the uploaded reading name.')
parser.add_argument('--date', type=str, help='Date of the reading.')
parser.add_argument('--frequency', type=str, help='Frequency of the reading.')
parser.add_argument('--dimension', type=str, help='Dimension of the reading.')
parser.add_argument('--input', type=int, help='Input for the reading.')

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

def input_to_json(input: int, dimension: str) ->List[List[int]]:
    import json    
    
    input = str(input)
    input_to_json = []
    if dimension in ['2','2.1', '2.2', '6', '8']:
        for i in range(0, 18, 3):
            row = [int(input[i]), int(input[i + 1]), int(input[i + 2])]
            input_to_json.append(row)
        return json.dumps(input_to_json)
    
    input = [list(map(int, list(x))) for x in input]
    return input


args = [
    'python', 'iching_engine.py', 
    'reading', 'new', 
    f'{name} ', '--date', date, '--frequency', frequency, '--dimension', dimension, '--input', input_to_json(int(input), dimension), '--input-type', 'json']

subprocess.run(args)
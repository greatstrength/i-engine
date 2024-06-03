import subprocess

batch = [
    {
        'name_prefix': '',
        'date': '',
        'frequency': '',
        'dimension': '',
        'input': ''
    }
]

for item in batch:

    subprocess.run(
        ['python', 'scripts/transcribe_reading_from_file.py'] +
        ['--name-prefix', item.get('name_prefix', None)] +
        ['--date', item.get('date', None)] +
        ['--frequency', item.get('frequency', None)] +
        ['--dimension', item.get('dimension', None)] +
        ['--input', item.get('input', None)]
    )
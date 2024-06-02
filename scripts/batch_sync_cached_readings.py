import subprocess
import yaml

with open('readings.yml', 'r') as f:
    readings = yaml.safe_load(f)
    if readings is None:
        readings = {}

    print(f"Syncing {len(readings)} readings")
    for key in readings.keys():
        if readings[key].get('synced', False):
            continue
        output, error = subprocess.Popen(
            ['python', 'iching_engine.py', 'reading', 'sync', key, '--remove-from-cache'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        if error:
            print(f"Error syncing reading {key}: {error}")
        else:
            print(f"Synced reading {key}")
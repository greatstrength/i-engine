import subprocess, json

reading_map = {

}

for id, input in reading_map.items():
    input = str(input)
    input_rows = []
    if len(input) != 36:
        for i in range(0, 18, 3):
            input_rows.append([int(input[i]), int(input[i + 1]), int(input[i + 2])])
    else:
        for i in range(0, 36, 6):
            input_rows.append([int(input[i]+input[i+1]), int(input[i + 2] + input[i+3]), int(input[i + 4]+ input[i+5])])
    print('Processing reading: ' + id)
    output, error = subprocess.Popen(['python', 'iching_engine.py', 'reading', 'add-results', id, "-i", json.dumps(input_rows), '--input-type', 'json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('Output: ' + output.decode('utf-8'))
    print('Error: ' + error.decode('utf-8'))
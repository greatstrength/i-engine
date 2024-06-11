from typing import List


def create_reading_input(input: str, dimension: str) -> List[List[int]]:
    if dimension in ['2', '2.1', '2.2', '6', '8']:
        result = []
        for i in range(0, 18, 3):
            row = [int(input[i]), int(input[i + 1]), int(input[i + 2])]
            result.append(row)
        return result
    elif dimension in ['49']:
        result = []
        for i in range(0, 36, 6):
            row = [int(input[i] + input[i + 1]),
                   int(input[i + 2] + input[i + 3]),
                   int(input[i + 4] + input[i + 5])
                   ]
            result.append(row)
        return result

    input = [list(map(int, list(x))) for x in input]
    return input

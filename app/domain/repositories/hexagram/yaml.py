from . import *

import yaml

class HexagramYamlRepository(HexagramRepository):

    def __init__(self, yaml_path: str):
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
            self.__data = {k: v for k, v in data.items()}
        

    def get(self, number: int) -> Hexagram:
        hex_data = self.__data.get(number, None)
        judgement = '\n'.join(hex_data.get('judgement', []))
        image = '\n'.join(hex_data.get('image', []))
        hex = Hexagram({
            'number': hex_data.get('number', 0),
            'name': hex_data.get('name', ''),
            'judgement': judgement,
            'image': image
        })

        lines_data = hex_data.get('changing_lines', [])
        for line_data in lines_data:
            line = Hexagram.Line({
                'yarrow_value': line_data.get('yarrow_value', 0),
                'line_number': line_data.get('line_number', 0)
            })
            line.text = '\n'.join(line_data.get('text', []))
            hex.changing_lines.append(line)

        return hex
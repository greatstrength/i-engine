from . import *

import yaml

class HexagramYamlRepository(HexagramRepository):

    def __init__(self, yaml_path: str):
        with open(yaml_path, 'r') as file:
            hexagrams = yaml.safe_load(file)
            self.__hexagrams = {k: Hexagram(v, strict=False) for k, v in hexagrams.items()}
        

    def get(self, number: int) -> Hexagram:
        return self.__hexagrams.get(number, None)
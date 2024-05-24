from . import *

from mondata.models import MondayModel
from mondata.types import NumberType
from mondata.types import TextType
from mondata.types import LongTextType
from mondata.types import SubItemType



class ChangingLineData(MondayModel):

    class Options():
        roles = {
            'read': wholelist(),
            'write': wholelist(),
        }

    position = NumberType(title = "Position")
    value = NumberType(title = "Value")
    text = TextType(title = "Translation")

    def map(self, role: str = 'read', **kwargs):
            
        obj = ChangingLine({
            'position': self.position,
            'value': self.value,
            'text': self.text['text'],
        })

        return obj


class HexagramData(MondayModel):

    class Options():
        roles = {
            'read': wholelist(),
            'write': wholelist(),
        }

    number = NumberType(title = "Number")
    judgement = LongTextType(title = "Judgement")
    image = LongTextType(title = "Image")
    secondary_names = TextType(title = "Secondary Names")
    changing_lines_ids = SubItemType(title = "Subitems")

    def map(self, role: str = 'read', changing_lines: List[ChangingLineData] = [], **kwargs):

        obj = Hexagram({
            'id': self.item.id,
            'number': self.number,
            'name': self.name,
            'judgement': self.judgement['text'],
            'image': self.image['text'],
            'secondary_names': self.secondary_names.split(', ') if self.secondary_names else [],
        })

        if changing_lines:
            obj.changing_lines = [line.map() for line in changing_lines]

        return obj


class MondataHexagramRepository(HexagramRepository):

    __cache = {}

    def __init__(self, monday_client, board_id: str):
        self.monday_client = monday_client
        self.load_cache(board_id)
        
    def load_cache(self, board_id):
        board = self.monday_client.get_board(board_id)
        hexagrams = board.get_items(get_column_values=True, limit=64, as_model=HexagramData)
        self.__cache = {int(hexagram.number): hexagram for hexagram in hexagrams}

    def get(self, number: int) -> Hexagram:
        hex_data: HexagramData = self.__cache.get(number, None)
        if not hex_data:
            return None

        changing_lines = []
        if hex_data.changing_lines_ids:
            changing_lines = self.monday_client.get_items(
                ids=hex_data.changing_lines_ids,
                as_model=ChangingLineData
            )

        return hex_data.map(changing_lines=changing_lines)
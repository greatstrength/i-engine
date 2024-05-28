from . import *

from schematics.transforms import wholelist, blacklist, whitelist
from mondata.models import MondayModel
from mondata.types import NumberType
from mondata.types import DateType
from mondata.types import DropdownType
from mondata.types import TextType
from mondata.types import ItemLinkType
from mondata.types import StatusType


class ResultLineData(MondayModel):

    class Options():
        serialize_when_none = False
        roles = {
            'read': wholelist(),
            'write': wholelist(),
        }

    position = NumberType(title = "Position")
    heaven_value = NumberType(title = "Heaven Value")
    man_value = NumberType(title = "Man Value")
    earth_value = NumberType(title = "Earth Value")
    line_value = NumberType(title = "Line Value")   

    def map(self, role: str = 'read', **kwargs):
        return ResultLine(dict(
            **kwargs,
            **self.to_primitive(role=role)
        ))


class ReadingResultData(MondayModel):

    class Options():
        serialize_when_none = False
        roles = {
            'read': wholelist(),
            'write': wholelist(),
        }

    date = DateType(title = "Date")
    type = DropdownType(title = "Type")
    frequency = DropdownType(title = "Time of Day")
    dimension = TextType(title = "Dimension")
    hexagram = ItemLinkType(title = "Hexagram")
    changing_hexagram = ItemLinkType(title = "Changing Hexagram")
    status = StatusType(title = "Status")

    def map(self, role: str = 'read', **kwargs):
        return ReadingResult(dict(
            **kwargs,
            **self.to_primitive(role=role)
        ))
    

class MondataReadingRepository(ReadingRepository):

    def __init__(self, monday_client, board_id: str):
        self.monday_client = monday_client
        self.board_id = board_id

    def save(self, reading: ReadingResult, group_type: str = 'Historical', no_input: bool = False):

        board = self.monday_client.get_board(self.board_id)
        if group_type == 'Historical':
            group_name = 'Historical Readings'
            group = board.get_group(title = group_name)

        reading_data = ReadingResultData(board=board)
        reading_data.name = reading.name
        reading_data.date = reading.date
        reading_data.type = [reading.type.capitalize()]
        reading_data.frequency = [reading.frequency.capitalize()]
        reading_data.dimension = reading.dimension
        reading_data.status = 'Entry Uploaded'
        reading_data.save(group=group)
        reading.id = reading_data.id

    def save_result_data(self, reading_id: str, result_data: List[ResultLine]):
        
        reading_data: ReadingResultData = self.monday_client.get_items(ids=[reading_id], as_model=ReadingResultData)[0]
        
        for line in result_data:
            item_name = f'{line.position}th Line'
            line_data: ResultLineData = reading_data.item.create_subitem(item_name, as_model=ResultLineData)
            line_data.position = line.position
            line_data.heaven_value = line.heaven_value
            line_data.man_value = line.man_value
            line_data.earth_value = line.earth_value
            line_data.line_value = line.line_value
            line_data.save()

    def set_hexagrams(self, reading_id: str, hexagram_id: str, changing_hexagram_id: str = None):
        
        reading_data: ReadingResultData = self.monday_client.get_items(ids=[reading_id], as_model=ReadingResultData)[0]
        reading_data.hexagram = hexagram_id
        if changing_hexagram_id:
            reading_data.changing_hexagram = changing_hexagram_id
        reading_data.status = 'Entered'
        reading_data.save()

    def upload_entry(self, reading_id: str, upload_file: str):

        reading_data: ReadingResultData = self.monday_client.get_items(ids=[reading_id], as_model=ReadingResultData)[0]
        file_value = reading_data.item.column_values['Original Entry']
        reading_data.item.add_file(file_value, upload_file)
        

"""I Ching Engine Hexagram Domain"""

# *** imports

# ** core
from typing import List, Optional

# ** infra
from pydantic import Field

# ** app
from tiferet.domain import DomainObject

# *** models

# ** model: changing_line
class ChangingLine(DomainObject):
    '''
    A changing line within an I Ching hexagram.
    '''

    # * attribute: text
    text: List[str] = Field(
        default_factory=list,
        description='The text lines associated with the changing line.',
    )

    # * attribute: yarrow_value
    yarrow_value: int = Field(
        ...,
        description='The yarrow stalk value of the changing line (6 or 9).',
    )

    # * attribute: line_number
    line_number: int = Field(
        ...,
        description='The position of the line in the hexagram (1 to 6).',
    )

    # * attribute: type
    type: Optional[str] = Field(
        default=None,
        description='The changing line type: reminder, warning, or null.',
    )


# ** model: hexagram
class Hexagram(DomainObject):
    '''
    An I Ching hexagram with judgement, image, and changing lines.
    '''

    # * attribute: number
    number: int = Field(
        ...,
        description='The traditional Wilhelm ordering number (1 to 64).',
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The primary name of the hexagram.',
    )

    # * attribute: secondary_names
    secondary_names: Optional[List[str]] = Field(
        default=None,
        description='Alternative names for the hexagram.',
    )

    # * attribute: judgement
    judgement: List[str] = Field(
        default_factory=list,
        description='The judgement text lines of the hexagram.',
    )

    # * attribute: image
    image: List[str] = Field(
        default_factory=list,
        description='The image text lines of the hexagram.',
    )

    # * attribute: changing_lines
    changing_lines: List[ChangingLine] = Field(
        default_factory=list,
        description='The six changing lines of the hexagram.',
    )

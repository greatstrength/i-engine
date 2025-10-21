"""I Ching Engine Hexagram Models"""

# *** imports

# ** infra
from tiferet import (
    ModelObject,
    StringType, 
    IntegerType, 
    ListType, 
    ModelType
)

# ** app
from .settings import HEXAGRAM_LINE_NUMBERS, HEXAGRAM_YARROW_VALUES

# *** models

# ** model: changing_line
class ChangingLine(ModelObject):
    '''
    A model object representing a changing line in an I Ching hexagram.
    '''

    # * attribute: text
    text = StringType(
        required=True,
        metadata=dict(
            description='The text associated with the changing line.'
        )
    )

    # * attribute: value
    value = IntegerType(
        required=True,
        choices=HEXAGRAM_YARROW_VALUES,
        metadata=dict(
            description='The yarrow stalk value of the changing line (6, 7, 8, or 9).'
        )
    )

    # * attribute: position
    position = IntegerType(
        required=True,
        choices=HEXAGRAM_LINE_NUMBERS,
        metadata=dict(
            description='The position of the line in the hexagram (1 to 6).'
        )
    )

    # * attribute: commentary
    commentary = StringType(
        metadata=dict(
            description='The commentary of the changing line.'
        )
    )

# ** model: trigram
class Trigram(ModelObject):
    '''
    A model object representing an I Ching trigram.
    '''

    # * attribute: id
    id = IntegerType(
        required=True,
        metadata=dict(
            description='The numerical value of the trigram (1 to 8).'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The name of the trigram.'
        )
    )

    # * attribute: family_member
    family_member = StringType(
        required=True,
        metadata=dict(
            description='The family member associated with the trigram.'
        )
    )

    # * attribute: element
    element = StringType(
        required=True,
        metadata=dict(
            description='The element associated with the trigram.'
        )
    )

    # * attribute: description
    description = StringType(
        required=True,
        metadata=dict(
            description='The description of the trigram.'
        )
    )

# ** model: hexagram
class Hexagram(ModelObject):
    '''
    A model object representing an I Ching hexagram.
    '''

    # * attribute: id
    id = IntegerType(
        required=True,
        metadata=dict(
            description='The numerical value of the hexagram (1 to 64).'
        )
    )

    # * attribute: name
    name = StringType(
        required=True,
        metadata=dict(
            description='The primary name of the hexagram.'
        )
    )

    # * attribute: secondary_names
    secondary_names = ListType(
        StringType(),
        default=[],
        metadata=dict(
            description='Alternative names for the hexagram.'
        )
    )

    # * attribute: judgement
    judgement = StringType(
        required=True,
        metadata=dict(
            description='The judgement text of the hexagram.'
        )
    )

    # * attribute: judgement_commentary
    judgement_commentary = StringType(
        required=True,
        metadata=dict(
            description='The commentary of the judgement text.'
        )
    )

    # * attribute: image
    image = StringType(
        required=True,
        metadata=dict(
            description='The image text of the hexagram.'
        )
    )

    # * attribute: image_commentary
    image_commentary = StringType(
        required=True,
        metadata=dict(
            description='The commentary of the image text.'
        )
    )

    # * attribute: changing_lines
    changing_lines = ListType(
        ModelType(ChangingLine),
        default=[],
        metadata=dict(
            description='List of changing lines in the hexagram.'
        )
    )

    # * attribute: upper_trigram
    upper_trigram = ModelType(
        Trigram,
        required=True,
        metadata=dict(
            description='The upper trigram of the hexagram.'
        )
    )

    # * attribute: lower_trigram
    lower_trigram = ModelType(
        Trigram,
        required=True,
        metadata=dict(
            description='The lower trigram of the hexagram.'
        )
    )
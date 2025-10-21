# *** imports

# ** core
import pytest

# ** app
from tiferet import ModelObject
from ..hexagram import (
    ChangingLine, 
    Trigram, 
    Hexagram
)

# *** fixtures

# ** fixture: changing_line
@pytest.fixture
def changing_line() -> ChangingLine:
    '''
    Fixture to create a basic ChangingLine object.
    '''
    
    # Create a ChangingLine instance.
    return ModelObject.new(
        ChangingLine,
        text='Test changing line',
        value=6,
        position=1,
        commentary='Test commentary'
    )

# ** fixture: trigram
@pytest.fixture
def trigram() -> Trigram:
    '''
    Fixture to create a basic Trigram object.
    '''
    
    # Create a Trigram instance.
    return ModelObject.new(
        Trigram,
        id=1,
        name='Qian',
        family_member='Father',
        element='Heaven',
        description='Creative and strong'
    )

# ** fixture: hexagram
@pytest.fixture
def hexagram(changing_line, trigram) -> Hexagram:
    '''
    Fixture to create a basic Hexagram object.
    '''
    
    # Create a Hexagram instance.
    return ModelObject.new(
        Hexagram,
        id=1,
        name='Qian',
        secondary_names=['The Creative'],
        judgement='Creative power brings success.',
        judgement_commentary='The creative force is strong.',
        image='The movement of heaven is full of power.',
        image_commentary='Heaven moves with strength and constancy.',
        changing_lines=[changing_line],
        upper_trigram=trigram,
        lower_trigram=trigram
    )

# *** tests

# ** test: changing_line_instantiation
def test_changing_line_instantiation(changing_line):
    '''
    Test successful instantiation of a ChangingLine object.
    '''
    
    # Verify attributes.
    assert isinstance(changing_line, ChangingLine)
    assert changing_line.text == 'Test changing line'
    assert changing_line.value == 6
    assert changing_line.position == 1
    assert changing_line.commentary == 'Test commentary'

# ** test: changing_line_required_fields
def test_changing_line_required_fields():
    '''
    Test validation of required fields in ChangingLine.
    '''
    
    # Test missing required text field.
    with pytest.raises(Exception):
        ModelObject.new(
            ChangingLine,
            value=6,
            position=1
        )

    # Test invalid value field.
    with pytest.raises(Exception):
        ModelObject.new(
            ChangingLine,
            text='Test line',
            value=5,  # Not in HEXAGRAM_YARROW_VALUES
            position=1
        )

    # Test invalid position field.
    with pytest.raises(Exception):
        ModelObject.new(
            ChangingLine,
            text='Test line',
            value=6,
            position=7  # Not in HEXAGRAM_LINE_NUMBERS
        )

# ** test: trigram_instantiation
def test_trigram_instantiation(trigram):
    '''
    Test successful instantiation of a Trigram object.
    '''
    
    # Verify attributes.
    assert isinstance(trigram, Trigram)
    assert trigram.id == 1
    assert trigram.name == 'Qian'
    assert trigram.family_member == 'Father'
    assert trigram.element == 'Heaven'
    assert trigram.description == 'Creative and strong'

# ** test: trigram_required_fields
def test_trigram_required_fields():
    '''
    Test validation of required fields in Trigram.
    '''
    
    # Test missing required id field.
    with pytest.raises(Exception):
        ModelObject.new(
            Trigram,
            name='Qian',
            family_member='Father',
            element='Heaven',
            description='Creative and strong'
        )

    # Test missing required name field.
    with pytest.raises(Exception):
        ModelObject.new(
            Trigram,
            id=1,
            family_member='Father',
            element='Heaven',
            description='Creative and strong'
        )

    # Test missing required family_member field.
    with pytest.raises(Exception):
        ModelObject.new(
            Trigram,
            id=1,
            name='Qian',
            element='Heaven',
            description='Creative and strong'
        )

    # Test missing required element field.
    with pytest.raises(Exception):
        ModelObject.new(
            Trigram,
            id=1,
            name='Qian',
            family_member='Father',
            description='Creative and strong'
        )

    # Test missing required description field.
    with pytest.raises(Exception):
        ModelObject.new(
            Trigram,
            id=1,
            name='Qian',
            family_member='Father',
            element='Heaven'
        )

# ** test: hexagram_instantiation
def test_hexagram_instantiation(hexagram, changing_line, trigram):
    '''
    Test successful instantiation of a Hexagram object.
    '''
    
    # Verify attributes.
    assert isinstance(hexagram, Hexagram)
    assert hexagram.id == 1
    assert hexagram.name == 'Qian'
    assert hexagram.secondary_names == ['The Creative']
    assert hexagram.judgement == 'Creative power brings success.'
    assert hexagram.judgement_commentary == 'The creative force is strong.'
    assert hexagram.image == 'The movement of heaven is full of power.'
    assert hexagram.image_commentary == 'Heaven moves with strength and constancy.'
    assert hexagram.changing_lines == [changing_line]
    assert hexagram.upper_trigram == trigram
    assert hexagram.lower_trigram == trigram

# ** test: hexagram_required_fields
def test_hexagram_required_fields(changing_line, trigram):
    '''
    Test validation of required fields in Hexagram.
    '''
    
    # Test missing required id field.
    with pytest.raises(Exception):
        ModelObject.new(
            Hexagram,
            name='Qian',
            judgement='Creative power brings success.',
            upper_trigram=trigram,
            lower_trigram=trigram
        )

    # Test missing required name field.
    with pytest.raises(Exception):
        ModelObject.new(
            Hexagram,
            id=1,
            judgement='Creative power brings success.',
            upper_trigram=trigram,
            lower_trigram=trigram
        )

    # Test missing required judgement/judgement_commentary fields.
    with pytest.raises(Exception):
        ModelObject.new(
            Hexagram,
            id=1,
            name='Qian',
            upper_trigram=trigram,
            lower_trigram=trigram
        )

    # Test missing required image/image_commentary fields.
    with pytest.raises(Exception):
        ModelObject.new(
            Hexagram,
            id=1,
            name='Qian',
            judgement='Creative power brings success.',
            upper_trigram=trigram,
            lower_trigram=trigram
        )

    # Test missing required upper_trigram field.
    with pytest.raises(Exception):
        ModelObject.new(
            Hexagram,
            id=1,
            name='Qian',
            judgement='Creative power brings success.',
            lower_trigram=trigram
        )

    # Test missing required lower_trigram field.
    with pytest.raises(Exception):
        ModelObject.new(
            Hexagram,
            id=1,
            name='Qian',
            judgement='Creative power brings success.',
            upper_trigram=trigram
        )
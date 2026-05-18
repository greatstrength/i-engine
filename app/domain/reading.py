"""I Ching Engine Reading Domain"""

# *** imports

# ** core
from datetime import date, datetime, timezone
from typing import Any, List, Optional

# ** infra
from pydantic import Field, model_validator

# ** app
from tiferet.domain import DomainObject

# *** models

# ** model: result_line
class ResultLine(DomainObject):
    '''
    A single line result within an I Ching reading.
    '''

    # * attribute: position
    position: int = Field(
        ...,
        description='The hexagram line position (1 to 6).',
    )

    # * attribute: heaven_line
    heaven_line: int = Field(
        ...,
        description='The heaven component value.',
    )

    # * attribute: man_line
    man_line: int = Field(
        ...,
        description='The man component value.',
    )

    # * attribute: earth_line
    earth_line: int = Field(
        ...,
        description='The earth component value.',
    )

    # * attribute: line_value
    line_value: int = Field(
        ...,
        description='The computed line value (6, 7, 8, or 9).',
    )


# ** model: hexagram_result
class HexagramResult(DomainObject):
    '''
    A hexagram reference within a reading result.
    '''

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the hexagram.',
    )

    # * attribute: number
    number: int = Field(
        ...,
        description='The Wilhelm index number of the hexagram.',
    )


# ** model: reading
class Reading(DomainObject):
    '''
    An I Ching reading with result lines and hexagram references.
    '''

    # * attribute: id
    id: Optional[str] = Field(
        default=None,
        description='The unique reading identifier (auto-generated if absent).',
    )

    # * attribute: name
    name: str = Field(
        ...,
        description='The name of the reading.',
    )

    # * attribute: dimension
    dimension: str = Field(
        ...,
        description='The dimension number for result line calculation.',
    )

    # * attribute: frequency
    frequency: str = Field(
        default='daily',
        description='The periodic frequency of the reading.',
    )

    # * attribute: type
    type: str = Field(
        default='general',
        description='The type of reading.',
    )

    # * attribute: date
    date: str = Field(
        ...,
        description='The date of the reading (ISO format).',
    )

    # * attribute: result_lines
    result_lines: List[ResultLine] = Field(
        default_factory=list,
        description='The computed result lines of the reading.',
    )

    # * attribute: current_or_previous
    current_or_previous: Optional[HexagramResult] = Field(
        default=None,
        description='The current or previous hexagram result.',
    )

    # * attribute: next
    next: Optional[HexagramResult] = Field(
        default=None,
        description='The next hexagram result.',
    )

    # * attribute: created_at
    created_at: str = Field(
        ...,
        description='ISO 8601 creation timestamp.',
    )

    # * method: _derive_defaults (validator)
    @model_validator(mode='before')
    @classmethod
    def _derive_defaults(cls, data: Any) -> Any:
        '''
        Derive default values for id, date, and created_at when absent.

        :param data: The raw input data.
        :type data: Any
        :return: The augmented input data.
        :rtype: Any
        '''

        # Only mutate dict-shaped inputs.
        if not isinstance(data, dict):
            return data
        data = dict(data)

        # Generate a UUID if id is not provided.
        if not data.get('id'):
            import uuid
            data['id'] = str(uuid.uuid4())

        # Default date to today.
        if not data.get('date'):
            data['date'] = date.today().isoformat()

        # Set timestamp if not provided.
        if not data.get('created_at'):
            data['created_at'] = datetime.now(timezone.utc).isoformat()

        # Return the augmented data.
        return data

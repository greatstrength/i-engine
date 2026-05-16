"""I Ching Engine Domain Constants"""

# *** constants

# ** constant: reading_result_dimensions
READING_RESULT_DIMENSIONS = [
    '2', '2.1', '2.2', '6', '8', '49'
]

# ** constant: reading_result_frequencies
READING_RESULT_FREQUENCIES = [
    'daily', 'weekly', 'morning', 'afternoon', 'evening', 'timeless'
]
READING_RESULT_FREQUENCY_DEFAULT = READING_RESULT_FREQUENCIES[0]

# ** constant: reading_result_types
READING_RESULT_TYPES = [
    'general', 'elemental', 'cardinal'
]
READING_RESULT_TYPE_DEFAULT = READING_RESULT_TYPES[0]

# ** constant: hexagram_yarrow_values
HEXAGRAM_YARROW_VALUES = [6, 9]

# ** constant: hexagram_line_numbers
HEXAGRAM_LINE_NUMBERS = [1, 2, 3, 4, 5, 6]

# ** constant: result_line_values
RESULT_LINE_VALUES = [6, 7, 8, 9]

# ** constant: two_d_transform
TWO_D_TRANSFORM = {
    False: 2,
    True: 3,
}

# ** constant: two_d_ext_1_transform
TWO_D_EXT_1_TRANSFORM = {
    1: 2, 2: 2, 3: 2,
    4: 3, 5: 3, 6: 3,
}

# ** constant: two_d_ext_2_transform
TWO_D_EXT_2_TRANSFORM = {
    1: 2, 2: 2, 3: 2, 4: 2,
    5: 3, 6: 3, 7: 3, 8: 3,
}

# ** constant: six_d_transform
SIX_D_TRANSFORM = {
    1: 3, 2: 2, 3: 3,
    4: 2, 5: 3, 6: 2,
}

# ** constant: eight_d_transform
EIGHT_D_TRANSFORM = {
    1: 3, 2: 2, 3: 3, 4: 2,
    5: 3, 6: 2, 7: 3, 8: 2,
}

# ** constant: forty_nine_d_transform
FORTY_NINE_D_TRANSFORM = {
    4: 2, 5: 2,
    8: 3, 9: 3,
}

# ** constant: transform_sum_to_lines
TRANSFORM_SUM_TO_LINES = {
    6: '--- X ---',
    7: '---------',
    8: '---   ---',
    9: '---( )---',
}

# ** constant: yarrow_to_hexagram_number
YARROW_TO_HEXAGRAM_NUMBER = {
    '887787': 55, '878878': 29, '878787': 63, '888877': 19,
    '888878': 7,  '887887': 51, '787878': 64, '787887': 21,
    '877777': 43, '787778': 50, '787787': 30, '777778': 44,
    '777878': 6,  '778888': 20, '777777': 1,  '888787': 36,
    '788778': 18, '788877': 41, '887878': 40, '878887': 3,
    '778878': 59, '887778': 32, '887888': 16, '778787': 37,
    '777787': 13, '877887': 17, '877888': 45, '778778': 57,
    '788787': 22, '778788': 53, '878888': 8,  '778887': 42,
    '877788': 31, '778877': 61, '777887': 25, '877877': 58,
    '788788': 52, '878877': 60, '887877': 54, '888788': 15,
    '878788': 39, '787877': 38, '877878': 47, '888777': 11,
    '787777': 14, '887777': 34, '877778': 28, '887788': 62,
    '787888': 35, '788887': 27, '888778': 46, '888888': 2,
    '777788': 33, '888887': 24, '877787': 49, '788888': 23,
    '777888': 12, '788777': 26, '778777': 9,  '777877': 10,
    '878777': 5,  '787788': 56, '878778': 48, '788878': 4,
}

# *** error codes

# ** constant: hexagram_not_found_id
HEXAGRAM_NOT_FOUND_ID = 'HEXAGRAM_NOT_FOUND'

# ** constant: hexagram_already_exists_id
HEXAGRAM_ALREADY_EXISTS_ID = 'HEXAGRAM_ALREADY_EXISTS'

# ** constant: invalid_hexagram_attribute_id
INVALID_HEXAGRAM_ATTRIBUTE_ID = 'INVALID_HEXAGRAM_ATTRIBUTE'

# ** constant: reading_not_found_id
READING_NOT_FOUND_ID = 'READING_NOT_FOUND'

# ** constant: reading_already_exists_id
READING_ALREADY_EXISTS_ID = 'READING_ALREADY_EXISTS'

# ** constant: invalid_reading_attribute_id
INVALID_READING_ATTRIBUTE_ID = 'INVALID_READING_ATTRIBUTE'

# ** constant: invalid_reading_input_id
INVALID_READING_INPUT_ID = 'INVALID_READING_INPUT'

# ** constant: invalid_reading_dimension_id
INVALID_READING_DIMENSION_ID = 'INVALID_READING_DIMENSION'

# ** constant: invalid_yarrow_value_id
INVALID_YARROW_VALUE_ID = 'INVALID_YARROW_VALUE'

# ** constant: kb_ingest_failed_id
KB_INGEST_FAILED_ID = 'KB_INGEST_FAILED'

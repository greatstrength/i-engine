# Environment
APP_ENV = 'APP_ENV'
DEFAULT_APP_ENV = 'prod'

# Configuration file
APP_CONFIGURATION_FILE = 'app/app.yml'

# Configuration
CONFIGS = 'configs' 
ENDPOINTS = 'endpoints'
ERRORS = 'errors'

# Dimension constants
DIMENSION_2 = '2'
DIMENSION_6 = '6'
DIMENSION_8 = '8'
DIMENSION_49 = '49'
DIMENSIONS = [DIMENSION_2, DIMENSION_6, DIMENSION_8, DIMENSION_49]

TWO_D_YARROW_TRANSFORM = {
    False: 2,
    True: 3
}

SIX_D_YARROW_TRANSFORM = {
    '1': 3,
    '2': 2,
    '3': 3,
    '4': 2,
    '5': 3,
    '6': 2
}

EIGHT_D_YARROW_TRANSFORM = {
    '1': 3,
    '2': 2,
    '3': 3,
    '4': 2,
    '5': 3,
    '6': 2,
    '7': 3,
    '8': 2
} 

FORTY_NINE_D_YARROW_TRANSFORM = {
    '4': 2,
    '5': 2,
    '8': 3,
    '9': 3
}

YARROW_SUM_TO_LINES = {
    6: '--- X ---',
    7: '---------',
    8: '---   ---',
    9: '---( )---'
}

TRANSFORM = {
    '2': TWO_D_YARROW_TRANSFORM,
    '6': SIX_D_YARROW_TRANSFORM,
    '8': EIGHT_D_YARROW_TRANSFORM,
    '49': FORTY_NINE_D_YARROW_TRANSFORM
}

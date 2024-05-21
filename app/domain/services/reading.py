from ..constants import *


def create_transform(dimension: str):
    if dimension == '2':
        return TWO_D_TRANSFORM
    if dimension == '6':
        return SIX_D_TRANSFORM
    if dimension == '8':
        return EIGHT_D_TRANSFORM
    if dimension == '49':
        return FORTY_NINE_D_TRANSFORM
    return None

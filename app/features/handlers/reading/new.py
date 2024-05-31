from ... import *
from .. import *


def handle(context: MessageContext):
    import os

    # Unpack request
    request: AddNewReading = context.data

    # Load reading cache repository.
    reading_cache: ReadingCache = context.services.reading_cache()

    # Load reading repository.
    reading_repo: ReadingRepository = context.services.reading_repo()

    # Load the hexagram repository.
    hexagram_repo: HexagramRepository = context.services.hexagram_repo()

    # Calculate summed transform.
    transform = reading_service.calculate_sum_transform(
        request.dimension, request.input) if not request.no_input else None

    # Create reading result.
    reading_result = reading_service.create_reading_result(
        transform=transform,
        **request.to_primitive())

    # # Save only reading to cloud should it not be cache only.
    if not request.cache_only:
        reading_repo.save(reading_result)

    reading_cache.save(reading_result)

    # Upload entry file if provided.
    if request.upload_file:
        reading_repo.upload_entry(reading_result.id, request.upload_file)
        if request.remove_file:
            os.remove(request.upload_file)

    # Return the result if the input data is not to be saved.
    if request.no_input:
        return reading_result

    # Save result data.
    reading_repo.save_result_data(
        reading_result.id, reading_result.result_lines)

    # Get reading hexagram.
    hex_number = hexagram_service.get_hexagram_number(reading_result)
    hexagram = hexagram_repo.get(hex_number)

    # Get changing hexagram.
    changing_hex_number = hexagram_service.get_changing_hexagram_number(
        reading_result)
    if changing_hex_number:
        changing_hexagram = hexagram_repo.get(changing_hex_number)
    else:
        changing_hexagram = None

    # Set hexagrams to reading result.
    reading_repo.set_hexagrams(
        reading_result.id,
        hexagram.id,
        changing_hexagram.id if changing_hexagram else None
    )

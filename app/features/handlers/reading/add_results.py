from ... import *
from .. import *


def handle(context: MessageContext):

    # Request.
    request: AddReadingResults = context.data

    # Load reading repository.
    reading_repo: ReadingRepository = context.services.reading_repo()

    # Load hexagram repository.
    hexagram_repo: HexagramRepository = context.services.hexagram_repo()

    # Load reading from repository.
    reading: ReadingResult = reading_repo.get(request.reading_id)

    # Calculate summed transform.
    transform = reading_service.calculate_sum_transform(
        reading.dimension, request.input) if request.input else None

    # Create reading result lines.
    result_lines = reading_service.create_result_lines(
        request.input, transform)

    # Save result data.
    reading_repo.save_result_data(
        request.reading_id, result_lines)

    # Get reading hexagram.
    hex_number = hexagram_service.get_hexagram_number(result_lines)
    hexagram = hexagram_repo.get(hex_number)

    # Get changing hexagram.
    changing_hex_number = hexagram_service.get_changing_hexagram_number(
        result_lines)
    if changing_hex_number:
        changing_hexagram = hexagram_repo.get(changing_hex_number)
    else:
        changing_hexagram = None

    # Set hexagrams to reading result.
    reading_repo.set_hexagrams(
        request.reading_id,
        hexagram.id,
        changing_hexagram.id if changing_hexagram else None
    )

from ... import *
from .. import *


def handle(context: MessageContext):

    # Request
    request: SyncReading = context.data

    # Load the reading cache.
    reading_cache: ReadingCache = context.services.reading_cache()

    # Load the reading repository.
    reading_repo: ReadingRepository = context.services.reading_repo()

    # Load the hexagram repository.
    hexagram_repo: HexagramRepository = context.services.hexagram_repo()

    # Load the reading.
    reading = reading_cache.get(request.reading_id)

    # Load the hexagram.
    current_no = hexagram_service.get_hexagram_number(reading.result_lines)
    current = hexagram_repo.get(current_no)

    # Load the changing hexagram.
    changing_no = hexagram_service.get_changing_hexagram_number(reading.result_lines)
    if current_no == changing_no:
        changing = None
    else:
        changing = hexagram_repo.get(changing_no) if changing_no else None

    # Save the reading.
    reading_repo.save(reading)

    # Update the result hexagrams.
    reading_repo.set_hexagrams(
        reading.id, current.id, changing.id if changing else None)

    # Save the result data.
    reading_repo.save_result_data(reading.id, reading.result_lines)

    # Upload the file if provided.
    if request.upload_file:
        reading_repo.upload_entry(reading.id, request.upload_file)

    # Delete the reading from the cache if not needed.
    if request.remove_from_cache:
        reading_cache.remove(request.reading_id)
    else:
        reading_cache.remove(request.reading_id)
        reading_cache.save(reading, synced=True)

    # Return the reading.
    return reading

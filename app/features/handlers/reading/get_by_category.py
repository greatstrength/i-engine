from ... import *
from .. import *

def handle(context: MessageContext):

    # Unpack request.
    request: GetReadingByCategory = context.data

    # Load reading repository.
    reading_repo: ReadingRepository = context.services.reading_repo()

    # Get readings by category.
    readings = reading_repo.get_by_category(
        request.date, request.type, request.frequency)
    
    # Return the first reading.
    return readings[0] if readings else None
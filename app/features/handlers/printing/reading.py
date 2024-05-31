from .. import *


def handle(context: MessageContext):

    # Request
    request: PrintReading = context.data

    # Get reading cache instance.
    reading_cache: ReadingCache = context.services.reading_cache()

    # Get hexagram repository instance.
    hexagram_repo: HexagramRepository = context.services.hexagram_repo()

    # Get result from cache.
    result = reading_cache.get(request.reading_id)

    # Old Printing Method
    is_changing, current, changing = printing_service.composite_to_composite_2d(
        result.result_lines)

    # Get current hexagram.
    current_no = printing_service.get_hexagram_number(current)
    current_hexagram = hexagram_repo.get(current_no)

    # Get changing hexagram.
    if is_changing:
        changing_no = printing_service.get_hexagram_number(changing)
        changing_hexagram = hexagram_repo.get(changing_no)

    print('\n')
    if is_changing:
        printing_service.print_changing_hexagran(
            result.result_lines, current_hexagram, changing_hexagram)
    else:
        printing_service.print_single_hexagram(result.result_lines, current_hexagram)

    # Null the result.
    context.result = None

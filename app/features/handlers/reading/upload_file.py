from ... import *
from .. import *

def handle(context: MessageContext):
    import os

    # Unpack request.
    request: UploadReadingFile = context.data

    # Load reading repository.
    reading_repo: ReadingRepository = context.services.reading_repo()

    # Upload entry file.
    reading_repo.upload_entry(request.reading_id, request.upload_file)

    # Remove the file if asked to.
    if request.remove_file:
        os.remove(request.upload_file)
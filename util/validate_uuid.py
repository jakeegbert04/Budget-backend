from uuid import UUID


def validate_uuid4(uuid_string, error_log=True):

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        if error_log:
            return False

    return val.hex == uuid_string.replace('-', '')
from uuid import UUID

def validate_uuid4(uuid_string):
    """
    Validate that uuid_string is a valid UUID.
    Accepts both string and UUID object.
    """
    try:
        # If it's already a UUID object, just check the version
        if isinstance(uuid_string, UUID):
            return uuid_string.version == 4
        
        # If it's a string, validate it
        val = UUID(uuid_string, version=4)
        return True
    except (ValueError, AttributeError, TypeError):
        return False
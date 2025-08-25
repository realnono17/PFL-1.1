def map_boolean(value):
    if value is None:
        return False
    val = str(value).strip().lower()
    return val in ["true", "yes", "1"]

def map_position(value):
    try:
        val = int(value)
        if val == 2:
            return "natural"
        elif val == 1:
            return "experienced"
        else:
            return "hidden"
    except (ValueError, TypeError):
        return "hidden"

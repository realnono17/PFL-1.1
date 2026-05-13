def map_boolean(value):
    """Convertit une valeur CSV en booléen (True/False)."""
    if value is None:
        return False
    val = str(value).strip().lower()
    return val in ["true", "yes", "1", "2"]   # 2 = natural (True)


def map_position(value):
    """
    Convertit une valeur CSV (2 = natural, 1 = experienced) en booléen.
    - True  : poste naturel (vert)
    - False : poste expérimenté (jaune)
    - None  : poste non applicable (caché)
    """
    try:
        val = int(value)
        if val == 2:
            return True       # natural
        elif val == 1:
            return False      # experienced
        else:
            return None       # hidden (non affiché)
    except (ValueError, TypeError):
        return None
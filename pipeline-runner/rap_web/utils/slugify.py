
def slugify(text):
    non_url_safe = ['"', '#', '$', '%', '&', '+', ',', '/', ':', ';', '=', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~', "'"]
    non_safe = [character for character in text if character in non_url_safe]
    if non_safe:
        for i in non_safe:
            text = text.replace(i, '')
    text = u'-'.join(text.split())
    return text.lower()


def filename_safe(unsafe_filename: str):
    allowed_characters = [' ', '.', '_', '-']
    safe_filename = ''.join(c for c in unsafe_filename if c.isalnum() or c in allowed_characters)
    return safe_filename

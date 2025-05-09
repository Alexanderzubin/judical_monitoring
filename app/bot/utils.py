import re


def is_valid_url(url: str) -> bool:
    pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.match(pattern, url) is not None

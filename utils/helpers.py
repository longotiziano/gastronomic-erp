def clean_string(input_string: str, title=False) -> str:
    input_string = input_string.strip()
    return input_string.title() if title else input_string.lower()
from datetime import date

def clean_string(input_string: str, title=False) -> str:
    input_string = input_string.strip()
    return input_string.title() if title else input_string.lower()

def format_date(date_obj: date) -> str:
    if date_obj is None:
        return "N/A"
    return date_obj.strftime("%d-%m-%Y")
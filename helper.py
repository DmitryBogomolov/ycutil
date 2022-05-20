from datetime import datetime


from datetime import datetime

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

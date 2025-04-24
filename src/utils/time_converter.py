from datetime import datetime, timezone
import re
from typing import Optional

def convert_to_unix_timestamp(time_str:str, date:str) -> int:
    # Format time string
    format = "%I:%M %p" 
    parsed_time = datetime.strptime(time_str, format).time()

    # Get todays date and combine to make datetime
    date_format = "%d/%m/%y"
    datetime_date = datetime.strptime(date, date_format).date()
    full_datetime = datetime.combine(datetime_date, parsed_time, tzinfo=timezone.utc)

    # Convert to timestamp
    unix_timestamp = int(full_datetime.timestamp())

    return unix_timestamp

def parse_duration(duration_span_raw: Optional[str]) -> Optional[int]:
    print("in parse duration method")
    if not duration_span_raw:
        print("no span?")
        return None
    
    # Normalising input
    duration_span_raw = re.sub(r'r/', '', duration_span_raw).strip().lower() # get rid of that weird r thing
    duration_span_raw = re.sub(r'\s+', ' ', duration_span_raw)


    hour_patterns = r"(?:hour[s]?|awr[s]?)"
    minute_patterns = r"(?:minute[s]?|munud[s]?)"

    full_match = re.search(rf"(\d+)\s*{hour_patterns}.*?(\d+)\s*{minute_patterns}", duration_span_raw)
    if full_match:

        hours = int(full_match.group(1))
        minutes = int(full_match.group(2))
        return hours*60 + minutes

    hour_match = re.search(rf'(\d)\s*{hour_patterns}', duration_span_raw)
    if hour_match:
        hours = int(hour_match.group(1))
        return hours*60
    
    minute_match = re.search(rf'(\d+)\s*{minute_patterns}', duration_span_raw)
    if minute_match:    
        minutes = int(minute_match.group(1))
        return minutes



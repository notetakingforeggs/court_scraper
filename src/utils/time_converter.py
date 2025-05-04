from datetime import datetime, timezone
import re
from typing import Optional

def normalise_start_time(start_time: str) -> str:
     
    m = re.match(
        r"""(?xi)
        ^\s*
        (\d{1,2})
        :(\d{1,2})
        (?: :\d{1,2})?
        \s*
        (am|pm)
        \s*
        $    
        """,
        start_time
    )
    if not m:
        raise ValueError(f"unexpected time format {start_time!r}")

    hour, minute, mer = m.groups()
    minute = minute.zfill(2)
    mer = mer.upper()
    clean_time = f"{hour}:{minute} {mer}"
    return clean_time

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
    if not duration_span_raw:
        print("parse duration: no duration span?")
        return None
    
    # Normalising input
    duration_span_raw = re.sub(r'r/', '', duration_span_raw).strip().lower() # get rid of that weird r thing
    duration_span_raw = re.sub(r'\s+', ' ', duration_span_raw)


    hour_patterns = r"(?:hour[s]?|awr[s]?)"
    minute_patterns = r"(?:minute[s]?|munud[s]?|min[s]?)"

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
# TODO this needs sorted out, probably just pass the entire time string to it and do the logic here before passing back start time and duration and appending them to the list.
def calculate_duration(start_and_end_times:str) -> tuple[str, int]:
    ''' takes in the string of eg... 12:00pm to 13:00pm and returns a tuple of start time and duration'''

    parts = re.split(r"\s*to\s*", start_and_end_times, flags=re.IGNORECASE)
    if len(parts) != 2:
        print("splitting start time/ end time produced unexpected output")
        return None 
    
    start_time = re.sub(r'(?i)(am|pm)$', r' \1', parts[0])
    end_time = re.sub(r'(?i)(am|pm)$', r' \1', parts[1])
    # print(f"start time: {start_time}, end time : {end_time}")

    fmt = "%I:%M %p"
    try:
        dt_start = datetime.strptime(start_time, fmt)
        dt_end = datetime.strptime(end_time, fmt)
        delta = dt_end - dt_start
        minutes = int(delta.total_seconds()) // 60
        return (start_time, minutes)
    except ValueError as e:
        print(f"value error! {e}")

 

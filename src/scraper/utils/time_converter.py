from datetime import datetime, timezone

def convert_to_unix_timestamp(time_str):

    # Format time string
    format = "%I:%M %p" 
    parsed_time = datetime.strptime(time_str, format).time()

    # Get todays date and combine to make datetime
    today_date = datetime.today().date()
    full_datetime = datetime.combine(today_date, parsed_time, tzinfo=timezone.utc)

    # Convert to timestamp
    unix_timestamp = int(full_datetime.timestamp())

    return unix_timestamp
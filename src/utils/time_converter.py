from datetime import datetime, timezone

def convert_to_unix_timestamp(time_str, date):
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
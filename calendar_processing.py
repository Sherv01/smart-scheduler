from ics import Calendar
from datetime import datetime, timedelta, time

def parse_ics_file(file_path):
    """Parse the .ics file and extract busy times."""
    with open(file_path, 'r') as f:
        calendar = Calendar(f.read())
    
    busy_times = []
    for event in calendar.events:
        busy_times.append((event.begin.datetime.replace(tzinfo=None), event.end.datetime.replace(tzinfo=None)))
    
    return busy_times

def generate_time_slots(start_time, end_time, increment_minutes=30):
    """Generate time slots between start_time and end_time."""
    current_time = start_time
    time_slots = []
    while current_time < end_time:
        time_slots.append(current_time)
        current_time += timedelta(minutes=increment_minutes)
    return time_slots

def get_free_times(busy_times, day, active_start, active_end, increment_minutes=30):
    """Generate a list of free times excluding busy times."""
    # Define the range of the day
    start_of_day = datetime.combine(day, time(0, 0))
    end_of_day = datetime.combine(day, time(23, 59))
    
    # Generate all potential time slots for the day
    all_time_slots = generate_time_slots(start_of_day, end_of_day, increment_minutes)

    # Filter time slots by user-defined active hours
    active_start_time = datetime.combine(day, active_start)
    active_end_time = datetime.combine(day, active_end)
    active_slots = [slot for slot in all_time_slots if active_start_time <= slot <= active_end_time]

    # Exclude busy times
    free_slots = []
    for slot in active_slots:
        if not any(start <= slot < end for start, end in busy_times):
            free_slots.append(slot)
    
    return free_slots

def format_free_times(free_times):
    """Format the free times for display."""
    return [f"{time.strftime('%H:%M')}" for time in free_times]

# Example usage
if __name__ == "__main__":
    ics_file = "C:/Users/Sherv/Desktop/Calendar Project/V2/test.ics"  # Replace with your file path
    day_to_check = datetime(2024, 10, 10).date()  # Replace with the date you want to check
    active_start = time(8, 0)  # User-defined active start time (e.g., 8 AM)
    active_end = time(22, 0)   # User-defined active end time (e.g., 10 PM)

    # Parse the .ics file to get busy times
    busy_times = parse_ics_file(ics_file)
    print("Busy times:")
    for start, end in busy_times:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}")

    # Get free times in 30-minute increments
    free_times = get_free_times(busy_times, day_to_check, active_start, active_end)

    # Format and print free times
    formatted_free_times = format_free_times(free_times)
    print("Free times:")
    for time_slot in formatted_free_times:
        print(time_slot)

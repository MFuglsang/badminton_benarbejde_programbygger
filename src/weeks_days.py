from datetime import datetime, timedelta, date  # Added `date` to the import
import calendar

def get_next_week_number():
    """
    Calculate the week number for the upcoming week based on the current date.

    Returns:
        int: The ISO week number of the next week.
    """
    today = datetime.now()
    next_week = today + timedelta(weeks=1)
    return next_week.isocalendar()[1]

def next_n_week_numbers(number_of_weeks):
    current_week_number = get_next_week_number()
    weeks = []
    for i in range(number_of_weeks):
        weeks.append(current_week_number + i)
    return weeks


def get_week_dates(week_number, year=None):
    """
    Get a dictionary of days and their dates for a given week number.

    Args:
        week_number (int): The ISO week number.
        year (int, optional): The year for the week. Defaults to the current year.

    Returns:
        dict: A dictionary where keys are weekdays (e.g., 'Monday') and values are their corresponding dates.
    """
    if year is None:
        year = datetime.now().year

    # Find the first day of the given week
    first_day_of_year = date(year, 1, 1)
    first_weekday = first_day_of_year.isoweekday()
    days_to_week_start = (week_number - 1) * 7 - (first_weekday - 1)
    week_start = first_day_of_year + timedelta(days=days_to_week_start)

    # Generate the dates for the week
    week_dates = {}
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        english_day = calendar.day_name[current_date.weekday()]
        danish_day = translate_day_to_danish(english_day)
        week_dates[english_day] = {
            "danish": danish_day,
            "date": current_date.strftime("%d-%m-%Y")
        }  # Separate keys for English, Danish, and date

    return week_dates

def translate_day_to_danish(english_day):
    """
    Translate an English day name to Danish.

    Args:
        english_day (str): The English name of the day (e.g., 'Monday').

    Returns:
        str: The Danish name of the day.
    """
    translations = {
        "Monday": "Mandag",
        "Tuesday": "Tirsdag",
        "Wednesday": "Onsdag",
        "Thursday": "Torsdag",
        "Friday": "Fredag",
        "Saturday": "Lørdag",
        "Sunday": "Søndag"
    }
    return translations.get(english_day, english_day)  # Default to English if no translation is found

# Example usage
if __name__ == "__main__":
    print("Next week's number:", get_next_week_number())
    week_number = get_next_week_number()
    print(f"Dates for week {week_number}:", get_week_dates(week_number))
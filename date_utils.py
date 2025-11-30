import sys
import re
from datetime import datetime


def parse_dates_from_args(args, logger=None):
    """
    Parses and validates one or more date arguments from the command line.
    Returns a list of valid date strings in YYYY-MM-DD format.
    If no arguments are provided, returns a list with today's date.
    Logs errors and exits on invalid input if logger is provided.

    Behavior:
    - If no dates are provided, returns [today's date].
    - If any invalid date is provided (wrong format or not a real date), logs an error and exits immediately.
    - If all dates are valid, returns the list of dates.
    - Never returns a partial list if any invalid date is present.
    """
    if len(args) == 1:
        today = datetime.today().strftime('%Y-%m-%d')
        if logger:
            logger.info(f"No date argument provided. Using today's date: {today} as default.")
        return [today]
    else:
        date_list = args[1:]
        valid_dates = []
        for d in date_list:
            if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
                try:
                    datetime.strptime(d, "%Y-%m-%d")
                    valid_dates.append(d)
                except ValueError:
                    if logger:
                        logger.error(f"Invalid date value: {d}. Please provide valid dates in YYYY-MM-DD format.")
                    sys.exit(1)
            else:
                if logger:
                    logger.error(f"Invalid date argument: {d}. Please provide dates in YYYY-MM-DD format.")
                sys.exit(1)
        return valid_dates
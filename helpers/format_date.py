from datetime import datetime


def format_date(date_string):
    format_try = ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y']
    for fmt in format_try:
        try:
            dt = datetime.strptime(date_string, fmt)
            break
        except ValueError:
            pass
    else:
        raise ValueError("Invalid date string format {}".format(date_string))

    return dt.strftime("%Y-%m-%d")

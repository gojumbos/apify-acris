

from datetime import datetime

# '%m %d %Y'
def curr_day():
    return datetime.now().strftime('%d')

def curr_month():
    return datetime.now().strftime('%m')

def curr_year():
    return datetime.now().strftime('%Y')

def curr_date():
    """
    month, day, year
    """
    return [curr_month(), curr_day(), curr_year()]


from datetime import date, timedelta

def get_available_dates(campaign):
    start = max(date.today(), campaign.start_date)
    end = campaign.end_date
    available_dates = []
    current = start
    if (end-start).days < 10:
        date_str = end.strftime('%Y-%m-%d')
        label = end.strftime('%B %d, %Y')
        available_dates.append((date_str, label))
        return available_dates
    else:
        while current <= end:
            date_str = current.strftime('%Y-%m-%d')
            label = current.strftime('%B %d, %Y')
            available_dates.append((date_str, label))
            current += timedelta(days=10)
        return available_dates

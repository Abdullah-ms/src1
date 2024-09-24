from datetime import date
from .models import Wisdom

def daily_wisdom():
    today = date.today()
    wisdoms = list(Wisdom.objects.all())
    if wisdoms:
        index = today.toordinal() % len(wisdoms)
        return wisdoms[index]
    return None

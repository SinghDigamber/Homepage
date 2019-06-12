from .models import calendar

# emojis
# 🏮 - hide from calendars
# 💎 - inIndex=True
# 🗃️ - inIndex=False (used at front-end only)
# 👤 — my activities

calendars = (
    calendar(
        title='SportEventsUA',
        title_full='Ukraine Sport Events',
        href='https://sportevent.com.ua/events/',
        emojis='💎'
    ),
    calendar(
        title='PrimeOrchestra',
        title_full='Расписание концертов Prime Orchestra',
        href='https://prime-orchestra.com/en/tours/',
        emojis='💎'
    ),
    calendar(
        title='ХТcal',
        title_full='Харьков-Турист (Heroku)',
        href='http://xtt.herokuapp.com/plan.ics',
        # parsed at http://xtt.herokuapp.com
        # real page at http://xt.ht/phpbb/viewforum.php?f=17
        emojis='💎'
    ),
    calendar(
        title='ИнтернетБилетХарьков',
        title_full='Интернет-Билет (Харьков)',
        href='https://kharkov.internet-bilet.ua',
        emojis='💎'
    ),
)

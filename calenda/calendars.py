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
    #calendar(
    #    title='МойКалендарь',
    #    title_full='Мой/Календарь',
    #    href='webcal://p23-calendars.icloud.com/published/2/AAAAAAAAAAAAAAAAAAAAADGKiNVIE_4PnUn5RgDzwhKEVCgLOwAw3XN5k3Fo7LNnLjiiSMubYE0h-TVQjc2xQsnURnMtPi-RoebOv3_f-Zk',
    #    emojis='💎'
    #),
    #calendar(
    #    title='МойРазвитие',
    #    title_full='Мой/Развитие',
    #    href='webcal://p23-calendars.icloud.com/published/2/AAAAAAAAAAAAAAAAAAAAADpDGy5wQRYJFPkAJFU_2jEZY8S66GOWvenhQ5U-9doIwmzgZOs5-v5UMrF1heVvNh_nPdSAWOKMflkgGbkD5q8',
    #    emojis='💎'
    #),
    #calendar(
    #    title='МойОтдых',
    #    title_full='Мой/Отдых',
    #    href='webcal://p23-calendars.icloud.com/published/2/AAAAAAAAAAAAAAAAAAAAAPQHJdmSH17t_eWUafno4QYmcmt3G29iA5HdqyeW-HUdQFnJuZyfZDNf3DUnI7_HuzN6dFJoakoQAs47wiuxl7k',
    #    emojis='💎'
    #),
    #calendar(
    #    title='ConcertUA',
    #    title_full='Concert.UA Харьков',
    #    href='https://concert.ua/ru/catalog/kharkiv/all-categories',
    #    emojis='💎'
    #),
    #calendar(
    #    title='Afisha057ua',
    #    title_full='Афиша 057.ua',
    #    href='https://www.057.ua/afisha/cat/2,3,4,5,6,7,8,9,26',
    #    emojis='💎'
    #),
    #calendar(
    #    title='TicketsUA',
    #    title_full='Tickets.UA Харьков',
    #    href='https://events.tickets.ua/harkov',
    #    emojis='💎'
    #),
)

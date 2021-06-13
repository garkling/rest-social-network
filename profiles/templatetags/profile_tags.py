from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag
def has_perms(request, obj):
    return request.user == obj


@register.filter
def convert_time(date):
    if date is None:
        return 'not logged yet'

    naive = date.replace(tzinfo=None, second=0, microsecond=0)
    now = datetime.now()
    dl = now - naive
    if now.day == naive.day:
        hours, remainder = divmod(dl.seconds, 3600)
        if not hours:
            minutes, seconds = divmod(remainder, 60)
            if not minutes:
                return f'{seconds} sec ago'
            return f'{minutes} min ago'

        if hours < 4:
            return f'{hours} h ago'

        return f'today at {naive.strftime("%H:%M")}'

    if now.day != naive.day or dl.days == 1:
        return f'yesterday at {naive.strftime("%H:%M")}'
    if naive.year != now.year:
        return naive.strftime("%H-%m-%d %H:%M")
    else:
        return naive.strftime("%m-%d %H:%M")

from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_relative_delta(time):
    delta = relativedelta(datetime.utcnow(), time)
    tme = []
    msg = time.strftime("%A, %B %d %Y @ %I:%M%p %Z")
    append_days = True
    if delta.years:
        years = delta.years
        tme.append(f"{years} years" if years != 1 else "1 year")
    if delta.months:
        months = delta.months
        tme.append(f"{months} months" if months != 1 else "1 month")
    if delta.days:
        days = delta.days
        tme.append(f"{days} days" if days != 1 else "1 day")
    if len(tme) == 0:
        append_days = False
        if delta.hours:
            hours = delta.hours
            tme.append(f"{hours} hours" if hours != 1 else "1 hour")
        if delta.minutes:
            minutes = delta.minutes
            tme.append(f"{minutes} minutes" if minutes != 1 else "1 minute")
        if delta.seconds:
            seconds = delta.seconds
            tme.append(f"{seconds} seconds" if seconds != 1 else "1 second")
    msg += f"\n{', '.join(tme)} ago"
    if append_days:
        if len(tme) != 1 and "days" not in tme[0]:
            msg += f" ({(datetime.utcnow() - time).days} days)"
    return msg


def get_bot_uptime(bot, *, brief=False):
    # Stolen from owner.py - Courtesy of Danny
    delta = datetime.utcnow() - bot.uptime
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    days, hours = divmod(hours, 24)
    minutes, seconds = divmod(remainder, 60)

    if not brief:
        if days:
            return f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"
        return f"{hours} hours, {minutes} minutes, and {seconds} seconds"
    if days:
        return f"{days} D - {hours} H - {minutes} M - {seconds} S"
    return f"{hours} H - {minutes} M - {seconds} S"

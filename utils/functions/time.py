import re
from datetime import datetime

from dateutil.relativedelta import relativedelta

from utils.functions.text import bold

__author__ = "Kanin"
__date__ = "11/19/2019"
__copyright__ = "Copyright 2019, Kanin"
__credits__ = ["Kanin"]
__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "Kanin"
__email__ = "im@kanin.dev"
__status__ = "Production"


# Wow this got bad, will rewrite later
def get_relative_delta(time, append_days: bool = False, append_long: bool = False,
                       append_small: bool = False, append_seconds: bool = True, bold_string: bool = False):
    past = False
    delta = relativedelta(time, datetime.utcnow())
    if datetime.utcnow() > time:
        past = True
        delta = relativedelta(datetime.utcnow(), time)
    tme = []
    msg = time.strftime("%A, %B %d %Y @ %I:%M%p %Z") if append_long else ""
    if delta.years:
        years = delta.years
        tme.append(f"{years} years" if years != 1 else "1 year")
    if delta.months:
        months = delta.months
        tme.append(f"{months} months" if months != 1 else "1 month")
    if delta.days:
        days = delta.days
        tme.append(f"{days} days" if days != 1 else "1 day")
    if len(tme) == 0 or append_small:
        if len(tme) == 0:
            append_days = False
        if delta.hours:
            hours = delta.hours
            tme.append(f"{hours} hours" if hours != 1 else "1 hour")
        if delta.minutes:
            minutes = delta.minutes
            tme.append(f"{minutes} minutes" if minutes != 1 else "1 minute")
        if delta.seconds and append_seconds:
            seconds = delta.seconds
            tme.append(f"{seconds} seconds" if seconds != 1 else "1 second")
    fixed = f"{', '.join(tme[:-1])}, and {tme[-1]}" if len(tme) > 2 else " and ".join(tme)
    msg += "in " if not past else ""
    msg += "\n" if append_long else ""
    msg += bold(fixed) if bold_string else fixed
    msg += " ago" if past else ""
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


def parse_time(time: str):
    years = months = weeks = days = hours = minutes = seconds = 0
    matches = re.findall(r"(\d+)(y|mo|w|d|h|m|s)", time)
    for match in matches:
        match_time = int(match[0])
        if match[1] == "y":
            years = 1
        elif match[1] == "mo":
            months = match_time if match_time <= 12 else 12
        elif match[1] == "w":
            weeks = match_time if match_time <= 52 else 52
        elif match[1] == "d":
            days = match_time if match_time <= 365 else 365
        elif match[1] == "h":
            hours = match_time if match_time <= 8766 else 8766
        elif match[1] == "m":
            minutes = match_time if match_time <= 525960 else 525960
        elif match[1] == "s":
            seconds = match_time if match_time <= 31557600 else 31557600
    return datetime.utcnow() + relativedelta(
        years=years, months=months, weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
    )

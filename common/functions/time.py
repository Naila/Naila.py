from datetime import datetime, timedelta, timezone


def float_to_discord_timestamp(seconds):
    now = datetime.now(timezone.utc)
    off = now + timedelta(seconds=seconds)
    return f"<t:{int(off.timestamp())}:R>"

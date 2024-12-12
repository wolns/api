from pytz import timezone

from src.core.config import get_timezone_settings

tz = timezone(get_timezone_settings().tz)

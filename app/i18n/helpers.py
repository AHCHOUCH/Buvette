from flask_login import current_user
from .translations import TRANSLATIONS

ROLE_LANG = {'admin': 'fr', 'cashier': 'ar'}

def lang():
    try:
        return ROLE_LANG.get(getattr(current_user, 'role', ''), 'fr') if current_user.is_authenticated else 'fr'
    except Exception:
        return 'fr'

def direction(language=None):
    return 'rtl' if (language or lang()) == 'ar' else 'ltr'

def translate(key, **kwargs):
    text = TRANSLATIONS.get(lang(), {}).get(key, key)
    return text.format(**kwargs) if kwargs else text

_ = translate

def weekday_key(index):
    return ['weekday.monday','weekday.tuesday','weekday.wednesday','weekday.thursday','weekday.friday','weekday.saturday','weekday.sunday'][int(index)]

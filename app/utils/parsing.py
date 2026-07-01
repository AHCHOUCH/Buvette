"""Safe request parsing helpers."""

def parse_required_int(value, error_key='error.required'):
    if value is None or str(value).strip() == '':
        raise ValueError(error_key)
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError('error.required')

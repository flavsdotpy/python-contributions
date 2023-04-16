from functools import reduce

def deep_get(dictionary, keys, default=None, target_type=None):
    value = reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary
    )
    return value if not target_type else target_type(value)

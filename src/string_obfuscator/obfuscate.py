import re
from functools import wraps
from typing import Dict, List


def obfuscate_fields(func):
    @wraps(func)
    def wrapper(payload: Dict, fields: List = None):
        for key, value in payload.items():
            if isinstance(value, dict):
                wrapper(value, fields)
            elif isinstance(value, list):
                for i in range(len(value)):
                    payload[key][i] = func(payload[key][i])
            else:
                if key in fields:
                    payload[key] = func(payload[key])

        return payload
    return wrapper


@obfuscate_fields
def obfuscate(text: str) -> str:
    text = str(text)
    size = int(len(text) / 2)
    return text.replace(
        text[-size:], re.sub(
            r'[a-zA-Z\d.,:;áéíóúàèìòùâêîôûãõ\-_]', '*', text[-size:]
        )).replace(' ', '*')

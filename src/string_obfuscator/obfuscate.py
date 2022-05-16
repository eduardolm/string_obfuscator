import re
from enum import Enum
from functools import wraps
from typing import Dict, List


def obfuscate_fields(func):
    @wraps(func)
    def wrapper(payload: Dict, fields: List = None, fields_enum: Enum = None) -> Dict:
        if not fields and not fields_enum:
            raise ValidationError(
                'Either a list or an enum must be passed to the method')
        if len(fields) == 0 and fields_enum:
            fields = [it.value for it in fields_enum]
        for key, value in payload.items():
            if isinstance(value, dict):
                wrapper(value, fields)
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], dict):
                        wrapper(value[i], fields)
                    else:
                        payload[key][i] = func(payload[key][i])
            else:
                if key in fields:
                    payload[key] = func(payload[key])

        return payload
    return wrapper


@obfuscate_fields
def obfuscate(text: str) -> str:
    """
    Method to obfuscate the values of corresponding keys.
    Method call requires either the list or the enum to be passed.
    If enum is to be used, an empty list [] should be passed as the second
    parameter, followed by the enum.
    :param payload: Dictionary object to obfuscate
    :param fields: List with keys which values should be obfuscated
    :param fields_enum: Enum with keys which values should be obfuscated
    :return: Dictionary with obfuscated fields
    """
    text = str(text)
    size = int(len(text) / 2)
    return text.replace(
        text[-size:], re.sub(
            r'[a-zA-Z\d.,:;áéíóúàèìòùâêîôûãõ\-_]', '*', text[-size:]
        )).replace(' ', '*')


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

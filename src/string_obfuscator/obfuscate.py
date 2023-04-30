import enum
import re
from functools import wraps
from typing import Dict


def obfuscate_fields(func):
    @wraps(func)
    def wrapper(payload: Dict, **kwargs) -> Dict:
        fields = kwargs.get('fields', None)
        if fields is None:
            raise ValidationError('Fields to obfuscate not informed. Either '
                                  'a list or enum containing the fields to '
                                  'obfuscate must be provided.')

        if isinstance(payload, dict) and isinstance(fields, (int, float)):
            raise ValidationError(f'Invalid parameter: "fields". Expected '
                                  f'type: list, enum, str when payload is'
                                  f' of type str. Provided '
                                  f'type: {type(fields)}')

        if not isinstance(fields, (list, enum.EnumMeta, str, int)):
            raise ValidationError(f'Invalid parameter: "fields". Expected '
                                  f'type: list, enum, str. Provided '
                                  f'type: {type(fields)}')

        if isinstance(payload, str) and isinstance(fields, str):
            return func(fields, payload)

        if payload is not None and isinstance(payload, str) and fields == 0:
            return func(payload)

        if isinstance(fields, enum.EnumMeta):
            fields = [it.value for it in fields]

        for key, value in payload.items():
            if isinstance(value, dict):
                wrapper(value, fields=fields)
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], dict):
                        wrapper(value[i], fields=fields)
                    else:
                        payload[key][i] = func(payload[key][i])
            else:
                if key in fields:
                    payload[key] = func(payload[key])

        return payload

    return wrapper


@obfuscate_fields
def obfuscate(text: str, payload: str = None) -> str:
    """
    Method to obfuscate the values of corresponding keys.
    Method call requires either the list or the enum to be passed.
    If enum is to be used, an empty list [] should be passed as the second
    parameter, followed by the enum.
    :param payload: Dictionary object to obfuscate. Payload can also be a
    plain string to be obfucated.
    :param fields: List or Enum with keys which values should be obfuscated.
    If parameter supplied is of type "str", obfuscates only the field with
    provided parameter as key. If payload is of type str, fields can be
    either str or 0. If field == 0, the payload will be obfuscated (Eg:
    payload is a document number and fields is 0).
    :return: Dictionary with obfuscated fields
    """
    text = str(text)
    size = int(len(text) / 2)
    pattern = re.compile(r'[a-zA-Z\d.,:;áéíóúàèìòùâêîôûãõ\-_]')

    if payload and isinstance(payload, str) and isinstance(text, str):
        return re.sub(text, text.replace(
            text[-size:], re.sub(pattern, '*', text[-size:])
        ).replace(' ', '*'), payload, count=len(payload))

    return text.replace(
        text[-size:], re.sub(pattern, '*', text[-size:])).replace(' ', '*')


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

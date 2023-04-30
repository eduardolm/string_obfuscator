# String Obfuscator

## Description
This module provides easy, out-of-the-box obfuscation solution for Python dicts.
It provides simple obfuscation algorithm to hide important information contained inside simple or nested dictionaries.
Works by replacing strings '*'.
This module obfuscates strings, integers, list items.

## How to use
This module was developed with easy-of-use in mind, so it's pretty straightforward:

Step-by-step guide:
+ `from string_obfuscator.obfuscate import obfuscate`
+ Dict can be obfuscated by calling: `obfuscate(dict_to_obfuscate, fields=list_with_keys_to_obfuscate)`

The `fields` argument can be a list, an enum, a string or 0.

If the argument provided is 0 and payload is str (Eg. document number), obfuscate returns obfuscated payload(str).
If the argument provided is of type string, only the existing dict items with keys matching the string will be obfuscated.
If the argument provided is of type list or enum, all the fields with corresponding keys in the dict_to_obfuscate will be obfuscated.

## Python version
This module was tested in Python 3.7, 3.8.5, 3.9
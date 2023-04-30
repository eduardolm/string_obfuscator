from enum import Enum
from unittest import TestCase

from src.string_obfuscator.obfuscate import obfuscate, ValidationError

FIELDS_LIST = ['name', 'document', 'id_number', 'email']
ENUM = Enum('ObfuscateName', {
    'NAME': 'name',
    'DOCUMENT': 'document',
    'ID_NUMBER': 'id_number',
    'EMAIL': 'email'})


class TestObfuscate(TestCase):

    def test_obfuscate_simple_dict(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }
        expected = {
            'document': '12345****',
            'email': 'test_email@********',
            'id_number': '123**',
            'name': 'Sample*T********'
        }

        response = obfuscate(test_dict, fields=FIELDS_LIST)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_simple_dict_passing_enum(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }
        expected = {
            'document': '12345****',
            'email': 'test_email@********',
            'id_number': '123**',
            'name': 'Sample*T********'
        }

        response = obfuscate(test_dict, fields=ENUM)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_dict_with_list_of_dict_passing_enum(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com',
            'list': [
                {
                    'name': 'Test Name',
                    'document': '55555555',
                    'age': 53
                },
                {
                    'name': 'Test Name Second',
                    'document': '4444444',
                    'age': 28
                }
            ]
        }
        expected = {
            'document': '12345****',
            'email': 'test_email@********',
            'id_number': '123**',
            'list': [
                {
                    'age': 53,
                    'document': '********',
                    'name': 'Test*****'
                },
                {
                    'age': 28,
                    'document': '******4',
                    'name': 'Test*Nam********'
                }
            ],
            'name': 'Sample*T********'
        }

        response = obfuscate(test_dict, fields=ENUM)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_should_raise_exception_if_no_parameters_supplied(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }

        with self.assertRaises(ValidationError):
            obfuscate(test_dict)

    def test_obfuscate_simple_dict_with_list(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': [
                '123456789',
                '987654321',
                '098723561'
            ],
            'id_number': 12345,
            'email': 'test_email@test.com'
        }
        expected = {
            'document': [
                '12345****',
                '98765****',
                '09872****'
            ],
            'email': 'test_email@********',
            'id_number': '123**',
            'name': 'Sample*T********'
        }

        response = obfuscate(test_dict, fields=FIELDS_LIST)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_nested_dict(self):
        test_dict = {
            'user_01': {
                'name': 'Sample Test Name',
                'document': [
                    '123456789',
                    '987654321',
                    '098723561'
                ],
                'id_number': 12345,
                'email': 'test_email@test.com'
            },
            'user_02': {
                'name': 'Sample Test Name 02',
                'document': [
                    '123456789',
                    '987654321',
                    '098723561'
                ],
                'id_number': 54321,
                'email': 'test_email_2@test.com'
            },
            'user_03': {
                'name': 'Sample Test Name',
                'document': [
                    '123456789',
                    '987654321',
                    '098723561'
                ],
                'id_number': 987456,
                'email': 'test_email_3@test.com'
            }

        }
        expected = {
            'user_01': {
                'document': [
                    '12345****',
                    '98765****',
                    '09872****'
                ],
                'email': 'test_email@********',
                'id_number': '123**',
                'name': 'Sample*T********'
            },
            'user_02': {
                'document': [
                    '12345****',
                    '98765****',
                    '09872****'
                ],
                'email': 'test_email_*@********',
                'id_number': '543**',
                'name': 'Sample*Tes*********'
            },
            'user_03': {
                'document': [
                    '12345****',
                    '98765****',
                    '09872****'
                ],
                'email': 'test_email_*@********',
                'id_number': '987***',
                'name': 'Sample*T********'
            }
        }

        response = obfuscate(test_dict, fields=FIELDS_LIST)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_raise_exception_if_payload_is_dict_fields_is_int(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }

        with self.assertRaises(ValidationError):
            obfuscate(test_dict, fields=1234)

    def test_obfuscate_raise_exception_if_payload_is_dict_fields_is_int_msg(
            self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }
        expected = f'Invalid parameter: "fields". Expected type: list, ' \
                   f'enum, str when payload is of type str. ' \
                   f'Provided type: {type(12)}'

        try:
            obfuscate(test_dict, fields=1234)
        except ValidationError as error:
            self.assertEqual(expected, error.message)

    def test_obfuscate_raise_exception_if_payload_is_dict_fields_is_float(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }

        with self.assertRaises(ValidationError):
            obfuscate(test_dict, fields=1234.0)

    def test_obfuscate_raise_exception_if_payload_is_dict_fields_is_float_msg(
            self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }
        expected = f'Invalid parameter: "fields". Expected type: list, ' \
                   f'enum, str when payload is of type str. Provided ' \
                   f'type: {type(12.0)}'

        try:
            obfuscate(test_dict, fields=1234.0)
        except ValidationError as error:
            self.assertEqual(expected, error.message)

    def test_obfuscate_simple_dict_with_str_passed_as_fields(self):
        test_dict = {
            'name': 'Sample Test Name',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }
        expected = {
            'name': 'Sample*T********',
            'document': '123456789',
            'id_number': 12345,
            'email': 'test_email@test.com'
        }

        response = obfuscate(test_dict, fields='name')

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_str_with_str_passed_as_fields_success(self):
        test_str = 'Test string to be obfuscated.'

        response = obfuscate(test_str, fields='string')

        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertEqual('Test str*** to be obfuscated.', response)

    def test_obfuscate_number_inside_str_with_str_passed_as_fields(self):
        document = '12345678921'
        test_str = f'Document is {document}'

        response = obfuscate(test_str, fields=document)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertEqual('Document is 123456*****', response)

    def test_obfuscate_number_inside_str_without_fields(self):
        document = '12345678921'

        response = obfuscate(document, fields=0)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertEqual('123456*****', response)


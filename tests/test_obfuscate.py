from enum import Enum
from unittest import TestCase

from src.string_obfuscator.obfuscate import obfuscate, ValidationError

FIELDS_LIST = ['name', 'document', 'id_number', 'email']
ENUM = Enum('ObfuscateName', {'name': 'name', 'document': 'document', 'id_number': 'id_number', 'email': 'email'})


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

        response = obfuscate(test_dict, FIELDS_LIST)

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

        response = obfuscate(test_dict, [], ENUM)

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

        response = obfuscate(test_dict, [], ENUM)

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
        test_dict_2 = {
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

        response = obfuscate(test_dict_2, FIELDS_LIST)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

    def test_obfuscate_nested_dict(self):
        test_dict_3 = {
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

        response = obfuscate(test_dict_3, FIELDS_LIST)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(expected, response)

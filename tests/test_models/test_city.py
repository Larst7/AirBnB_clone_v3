#!/usr/bin/python3
"""
Unit Test for City Class
"""
import unittest
from datetime import datetime
import models
import json
import os

City = models.city.City
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class TestCityDocs(unittest.TestCase):
    """Class for testing City docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('........   City Class   ........')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nCity Class from Models Module\n'
        actual = models.city.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'City class handles all application cities'
        actual = City.__doc__
        self.assertEqual(expected, actual)


class TestCityInstances(unittest.TestCase):
    """Testing City class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('.........  City Class  .........')
        print('.................................\n\n')

    def setUp(self):
        """Initialize a new city for testing"""
        self.city = City()

    def test_instantiation(self):
        """Check if City is properly instantiated"""
        self.assertIsInstance(self.city, City)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_string(self):
        """Check if BaseModel is properly casted to string"""
        my_str = str(self.city)
        my_list = ['City', 'id', 'created_at']
        actual = sum(sub_str in my_str for sub_str in my_list)
        self.assertEqual(3, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """Check that it should not have updated attribute"""
        my_str = str(self.city)
        actual = 'updated_at' not in my_str
        self.assertTrue(actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """Check if save function adds updated_at attribute"""
        self.city.save()
        actual = isinstance(self.city.updated_at, datetime)
        self.assertTrue(actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """Check if to_json returns serializable dict object"""
        self.city_json = self.city.to_json()
        actual = isinstance(self.city_json, dict)
        self.assertTrue(actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """Check if to_json includes class key with value City"""
        self.city_json = self.city.to_json()
        actual = self.city_json.get('__class__')
        self.assertEqual('City', actual)

    def test_state_attribute(self):
        """Check addition of state attribute"""
        self.city.state_id = 'IL'
        actual = self.city.state_id
        self.assertEqual('IL', actual)


if __name__ == '__main__':
    unittest.main()

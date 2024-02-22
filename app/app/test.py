"""Sample tests"""

from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""
    def test_add_numbers(self):
        """Test adding numbers"""
        res = calc.add(2, 8)
        self.assertEqual(res, 10)

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(25, 10)
        self.assertEqual(res, 15)

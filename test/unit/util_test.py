import unittest
import pytest

from app.util import Util


@pytest.mark.unit
class TestUtil(unittest.TestCase):
    def test_convert_to_number_correct_param(self):
        self.assertEqual(4, Util.convert_to_number("4"))
        self.assertEqual(0, Util.convert_to_number("0"))
        self.assertEqual(0, Util.convert_to_number("-0"))
        self.assertEqual(-1, Util.convert_to_number("-1"))
        self.assertAlmostEqual(4.0, Util.convert_to_number("4.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, Util.convert_to_number("0.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, Util.convert_to_number("-0.0"), delta=0.0000001)
        self.assertAlmostEqual(-1.0, Util.convert_to_number("-1.0"), delta=0.0000001)

    def test_convert_to_number_invalid_type(self):
        self.assertRaises(TypeError, Util.convert_to_number, "")
        self.assertRaises(TypeError, Util.convert_to_number, "3.h")
        self.assertRaises(TypeError, Util.convert_to_number, "s")
        self.assertRaises(TypeError, Util.convert_to_number, None)
        self.assertRaises(TypeError, Util.convert_to_number, object())

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
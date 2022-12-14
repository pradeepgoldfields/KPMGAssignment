import unittest
import DeepFind as ExerciseClass
import json


class Test(unittest.TestCase):
    e = ExerciseClass.Exercise3()
    def test_0_get_nested_value(self):
        self.assertEqual(3, self.e.get_nested_value({'a': 0, 'b': [1, {"c":3}, 2]}, "b/c"))

    def test_1_get_nested_value(self):
        self.assertEqual(1, self.e.get_nested_value({"a": {"b": {"c": 1}}}, "a/b/c"))

    def test_3_get_nested_value(self):
        self.assertEqual([3, 1], self.e.get_nested_value({'a': 0, 'b': [1, {"c": [3, 1]}, 2]}, "b/c"))

    def test_4_get_nested_value(self):
        self.assertEqual(None, self.e.get_nested_value({'a': 0, 'b': [1, {"c": [3, 1]}, 2]}, "b/d"))


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
import unittest
import InstanceMetadataAndDeepFind as ExerciseClass
import json


class Test(unittest.TestCase):
    e = ExerciseClass.Exercise()
    def test_0_get_nested_value(self):
        self.assertEqual(1, self.e.get_nested_value(json.dumps({"a": {"b": {"c": 1}}}), "a/b/c"))

    def test_1_get_nested_value(self):
        self.assertEqual([1, 2], self.e.get_nested_value(json.dumps({'a': 0, 'b': [[1, 2]]}), "b/0/1"))


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
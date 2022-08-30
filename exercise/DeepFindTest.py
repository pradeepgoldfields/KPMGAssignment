# import Exercise as ExerciseClass
import json
import unittest

class Test(unittest.TestCase):
    e = Exercise()
    def test_0_get_nested_value(self):
        self.assertEqual(1, self.e.get_nested_value(json.dumps({"a": {"b": {"c": 1}}}), "a/b/c"))
        self.assertEqual([1, 2], self.e.get_nested_value(json.dumps({'a': 0, 'b': [[1, 2]]}), "b/0/1"))


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
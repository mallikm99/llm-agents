import unittest

from src.data_utils import load_functions_from_directory


class TestLoadFunctionsFromDirectory(unittest.TestCase):

    def test_load_functions_from_directory(self):
        # Call the function under test
        tools = load_functions_from_directory("functions")

        # Debugging: Print all tools to inspect them
        self.assertEqual(len(tools), 30)  # change this number as you add more functions


if __name__ == "__main__":
    unittest.main()

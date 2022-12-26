import unittest
import src.iToppy.main as tpl_main

class TestMain(unittest.TestCase):
    def setUp(self):
        self.values = [
            {
                "input": ("Hello World!", 3),
                "expect": "Hello World!Hello World!Hello World!"
            },
            {
                "input": ("Hello World!", 0),
                "expect": ""
            },
            {
                "input": ("Hello World!", -1),
                "expect": ""
            }
        ]

    def test_main(self):
        self.assertEqual(True, True)
        # for item in self.values:
        #     tester = tpl_main.PythonTemplate(item["input"][0])
        #     self.assertEqual(
        #         tester.get_x_times(item["input"][1]),
        #         item["expect"]
        #     )
            
    def test_failure(self):
        self.assertEqual(True, False)
        # with self.assertRaises(TypeError):
        #     tester = tpl_main.PythonTemplate(Exception)
        #     tester.get_x_times(10)
            
if __name__ == '__main__':
    unittest.main()
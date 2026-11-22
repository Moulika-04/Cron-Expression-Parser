import unittest

from cron_parser import (
    CronExpressionError,
    get_field_values,
    display_result,
    parse_cron,
)

class ExpandFieldTests(unittest.TestCase):
    def test_wildcard(self):
        self.assertEqual(get_field_values("*", 1, 5), [1, 2, 3, 4, 5])

    def test_step(self):
        self.assertEqual(get_field_values("*/15", 0, 59), [0, 15, 30, 45])

    def test_comma_list(self):
        self.assertEqual(get_field_values("1,15", 1, 31), [1, 15])

    def test_range(self):
        self.assertEqual(get_field_values("1-5", 0, 7), [1, 2, 3, 4, 5])

    def test_range_with_step(self):
        self.assertEqual(get_field_values("2-10/2", 0, 12), [2, 4, 6, 8, 10])

    def test_single_value_with_step(self):
        self.assertEqual(get_field_values("5/10", 0, 30), [5, 15, 25])

    def test_combined_items_are_sorted_and_unique(self):
        self.assertEqual(get_field_values("1,3-5,*/2", 0, 6), [0, 1, 2, 3, 4, 5, 6])

    def test_invalid_values(self):
        for expression in ("60", "*/0", "5-2", "abc", "1,,2", "1/abc"):
            with self.subTest(expression=expression):
                with self.assertRaises(CronExpressionError):
                    get_field_values(expression, 0, 59)

class ParseExpressionTests(unittest.TestCase):
    def test_sample_expression(self):
        rows = parse_cron("*/15 0 1,15 * 1-5 /usr/bin/find")
        self.assertEqual(rows, [
            ("minute", "0 15 30 45"),
            ("hour", "0"),
            ("day of month", "1 15"),
            ("month", "1 2 3 4 5 6 7 8 9 10 11 12"),
            ("day of week", "1 2 3 4 5"),
            ("command", "/usr/bin/find"),
        ])

    def test_command_can_contain_spaces(self):
        rows = parse_cron("0 0 * * * echo hello world")
        self.assertEqual(rows[-1], ("command", "echo hello world"))

    def test_wrong_number_of_parts(self):
        with self.assertRaises(CronExpressionError):
            parse_cron("* * * * *")

    def test_formatting(self):
        output = display_result([("minute", "0 15"), ("command", "/bin/run")])
        self.assertEqual(output, "minute        0 15\ncommand       /bin/run")

if __name__ == "__main__":
    unittest.main()




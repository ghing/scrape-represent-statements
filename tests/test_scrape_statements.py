import unittest

from represent_statements.cli.scrape_statements import parse_date


class TestHelpers(unittest.TestCase):
    def test_parse_date(self):
        d = parse_date('Oct. 8, 2013')
        self.assertEqual(d, '2013-10-08')

        d = parse_date('Feb. 13')
        self.assertEqual(d, '2017-02-13')

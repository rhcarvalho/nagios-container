#!/usr/bin/env python
import unittest

from disk_usage import analize, parse_df


class TestAnalize(unittest.TestCase):

    def runTest(self):
        self.assertEqual(analize(0, 0, 0, 0), (True, True))
        self.assertEqual(analize(1, 0, 0, 0), (True, True))
        self.assertEqual(analize(15, 48, 0, 0), (True, True))
        self.assertEqual(analize(15, 48, 80, 90), (False, False))
        self.assertEqual(analize(100, 48, 80, 99), (True, True))
        self.assertEqual(analize(48, 100, 80, 99), (True, True))
        self.assertEqual(analize(100, 48, 80, 100), (True, True))


class TestParseDf(unittest.TestCase):

    def runTest(self):
        self.assertEqual(parse_df(r"Mounted on     Use% IUse%"), ())
        self.assertEqual(parse_df(r"/                1%    1%"), ("/", 1, 1))
        self.assertEqual(parse_df(r"/etc/hosts      19%    8%"), ("/etc/hosts", 19, 8))


if __name__ == "__main__":
    unittest.main()

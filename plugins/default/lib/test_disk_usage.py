#!/usr/bin/env python
import unittest

from disk_usage import analize, parse_df_line, parse_df_lines, report


class TestAnalize(unittest.TestCase):

    def runTest(self):
        self.assertEqual(analize(
            'pod-a1b2c', [['/', 0, 0], ['/b', 15, 48]], 0, 0),
            ([['pod-a1b2c', '/', 0, 0, 2], ['pod-a1b2c', '/b', 15, 48, 2]]))
        self.assertEqual(analize(
            'pod-a1b2c', [['/', 0, 0], ['/b', 15, 48]], 20, 50),
            ([['pod-a1b2c', '/', 0, 0, 0], ['pod-a1b2c', '/b', 15, 48, 1]]))
        self.assertEqual(analize(
            'pod-a1b2c', [['/', 0, 0], ['/b', 15, 48]], 80, 90),
            ([['pod-a1b2c', '/', 0, 0, 0], ['pod-a1b2c', '/b', 15, 48, 0]]))


class TestParseDfLine(unittest.TestCase):

    def runTest(self):
        self.assertEqual(parse_df_line(
            r"Use% IUse% Mounted on"),
            ())
        self.assertEqual(parse_df_line(
            r"  1%    1% /"),
            ("/", 1, 1))
        self.assertEqual(parse_df_line(
            r" 10%    1% /etc/hosts"),
            ("/etc/hosts", 10, 1))
        self.assertEqual(parse_df_line(
            r"  1%    1% /run/secrets/kubernetes.io/serviceaccount"),
            ("/run/secrets/kubernetes.io/serviceaccount", 1, 1))
        self.assertEqual(parse_df_line(
            r"  1%    1% /etc/feedhenry/gitlab-shell"),
            ("/etc/feedhenry/gitlab-shell", 1, 1))


class TestParseDfLines(unittest.TestCase):

    def runTest(self):
        self.assertEqual(parse_df_lines(
            "Use% IUse% Mounted on\n"
            "  1%    1% /\n"
            " 19%    8% /etc/hosts\n"
            "  1%    1% /run/secrets/kubernetes.io/serviceaccount"),
            [("/", 1, 1), ("/etc/hosts", 19, 8), ("/run/secrets/kubernetes.io/serviceaccount", 1, 1)])


class TestReport(unittest.TestCase):

    def runTest(self):
        self.assertEqual(
            report([['xyz', '/a', 0, 0, 0], ['xyz', '/b', 15, 48, 0]]), 0)
        self.assertEqual(
            report([['xyz', '/a', 0, 0, 0], ['xyz', '/b', 15, 48, 1]]), 1)
        self.assertEqual(
            report([['xyz', '/a', 0, 0, 2], ['xyz', '/b', 15, 48, 2]]), 2)
        self.assertEqual(
            report([['xyz', '/a', 0, 0, 2], ['xyz', 'fake_unknown', 0, 0, 3]]), 3)

if __name__ == "__main__":
    unittest.main()

# TODO: Try to find a theoretically valid case for TestReport result of 3
# (nagios.UNKNOWN)

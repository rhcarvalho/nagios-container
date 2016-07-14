#!/usr/bin/env python
import unittest

from mongodb_health import analize, parse_mongo_result, report, REPLSET_STATUS
import nagios


class TestAnalize(unittest.TestCase):

    def runTest(self):
        self.assertEqual(analize(REPLSET_STATUS.STARTUP), nagios.WARN)
        self.assertEqual(analize(REPLSET_STATUS.PRIMARY), nagios.OK)
        self.assertEqual(analize(REPLSET_STATUS.SECONDARY), nagios.OK)
        self.assertEqual(analize(REPLSET_STATUS.RECOVERING), nagios.CRIT)
        self.assertEqual(analize(REPLSET_STATUS.FATAL), nagios.CRIT)
        self.assertEqual(analize(REPLSET_STATUS.STARTUP2), nagios.CRIT)
        self.assertEqual(analize(REPLSET_STATUS.UNKNOWN), nagios.CRIT)
        self.assertEqual(analize(REPLSET_STATUS.ARBITER), nagios.WARN)
        self.assertEqual(analize(REPLSET_STATUS.DOWN), nagios.CRIT)
        self.assertEqual(analize(REPLSET_STATUS.ROLLBACK), nagios.CRIT)
        self.assertEqual(analize(REPLSET_STATUS.REMOVED), nagios.CRIT)
        self.assertEqual(analize(None), nagios.UNKNOWN)


class TestParseMongoResult(unittest.TestCase):

    def runTest(self):
        self.assertEqual(parse_mongo_result("0\n"), REPLSET_STATUS.STARTUP)
        self.assertEqual(parse_mongo_result("1\n"), REPLSET_STATUS.PRIMARY)
        self.assertEqual(parse_mongo_result("2\n"), REPLSET_STATUS.SECONDARY)
        self.assertEqual(parse_mongo_result("3\n"), REPLSET_STATUS.RECOVERING)
        self.assertEqual(parse_mongo_result("4\n"), REPLSET_STATUS.FATAL)
        self.assertEqual(parse_mongo_result("5\n"), REPLSET_STATUS.STARTUP2)
        self.assertEqual(parse_mongo_result("6\n"), REPLSET_STATUS.UNKNOWN)
        self.assertEqual(parse_mongo_result("7\n"), REPLSET_STATUS.ARBITER)
        self.assertEqual(parse_mongo_result("8\n"), REPLSET_STATUS.DOWN)
        self.assertEqual(parse_mongo_result("9\n"), REPLSET_STATUS.ROLLBACK)
        self.assertEqual(parse_mongo_result("10\n"), REPLSET_STATUS.REMOVED)
        self.assertEqual(parse_mongo_result("\n"), None)
        self.assertEqual(parse_mongo_result(""), None)


class TestReport(unittest.TestCase):

    def runTest(self):
        self.assertEqual(
            report(
                pods=("mongodb-1-1-s1ngl",),
                rs_statuses=(REPLSET_STATUS.PRIMARY,),
                nag_statuses=(nagios.OK,),
            ), nagios.OK)
        self.assertEqual(report(
                pods=("mongodb-1-1-9hj1x", "mongodb-2-1-xu70c", "mongodb-3-1-wdq55"),
                rs_statuses=(REPLSET_STATUS.PRIMARY, REPLSET_STATUS.SECONDARY, REPLSET_STATUS.SECONDARY),
                nag_statuses=(nagios.OK, nagios.OK, nagios.OK)
            ), nagios.OK)
        self.assertEqual(report(
                pods=("mongodb-1-1-9hj1x", "mongodb-2-1-xu70c", "mongodb-3-1-wdq55"),
                rs_statuses=(REPLSET_STATUS.PRIMARY, REPLSET_STATUS.SECONDARY, REPLSET_STATUS.PRIMARY),
                nag_statuses=(nagios.OK, nagios.OK, nagios.OK)
            ), nagios.CRIT)
        self.assertEqual(report(
                pods=("mongodb-1-1-9hj1x", "mongodb-2-1-xu70c"),
                rs_statuses=(REPLSET_STATUS.PRIMARY, REPLSET_STATUS.SECONDARY),
                nag_statuses=(nagios.OK, nagios.OK)
            ), nagios.WARN)
        self.assertEqual(report(
                pods=("mongodb-1-1-9hj1x", "mongodb-2-1-xu70c", "mongodb-3-1-wdq55"),
                rs_statuses=(REPLSET_STATUS.PRIMARY, REPLSET_STATUS.SECONDARY, REPLSET_STATUS.SECONDARY),
                nag_statuses=(nagios.WARN, nagios.OK, nagios.OK)
            ), nagios.WARN)
        self.assertEqual(report(
                pods=("mongodb-1-1-9hj1x", "mongodb-2-1-xu70c", "mongodb-3-1-wdq55"),
                rs_statuses=(REPLSET_STATUS.PRIMARY, REPLSET_STATUS.ARBITER, REPLSET_STATUS.SECONDARY),
                nag_statuses=(nagios.OK, nagios.WARN, nagios.OK)
            ), nagios.WARN)
        self.assertEqual(report(
                pods=("mongodb-1-1-9hj1x", "mongodb-2-1-xu70c"),
                rs_statuses=(REPLSET_STATUS.PRIMARY,),
                nag_statuses=(nagios.OK, nagios.UNKNOWN)
            ), nagios.UNKNOWN)
        self.assertEqual(report(
                pods=(),
                rs_statuses=(),
                nag_statuses=()
            ), nagios.UNKNOWN)


if __name__ == "__main__":
    unittest.main()

import sys
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(cur_dir, os.pardir))
import unishark
import unittest
import logging
from time import sleep

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def setUpModule():
    print('%s.setUpModule' % __name__)
    sleep(0.1)


def tearDownModule():
    print('%s.tearDownModule' % __name__)
    sleep(0.1)


class MyTestClass3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('\t%s.%s.setUpClass' % (__name__, cls.__name__))
        sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        print('\t%s.%s.tearDownClass' % (__name__, cls.__name__))
        sleep(0.1)

    def test_5(self):
        """Here is test_5's doc str"""
        log.error('This is a case having an error that is not AssertionError. '
                  'unittest distinguishes "failure" and "error" by if the case raises an AssertionError or not.')
        sleep(1)
        raise TypeError

    def test_6(self):
        """Here is test_6's doc str"""
        log.info('Here is logging of test_6')
        sleep(1)
        self.assertEqual(1, 1)

    @unittest.skip("Reason of skipping 'test_7'")
    def test_7(self):
        """Here is test_7's doc str"""
        sleep(3)
        self.assertEqual(1, 1)


class MyTestClass4(MyTestClass3):
    @classmethod
    def setUpClass(cls):
        print('\t%s.%s.setUpClass' % (__name__, cls.__name__))
        sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        print('\t%s.%s.tearDownClass' % (__name__, cls.__name__))
        sleep(0.1)

    @unittest.expectedFailure
    def test_8(self):
        """Here is test_8's doc str"""
        log.error('This is unexpected to be passed.')
        sleep(1)
        self.assertEqual(1, 1)

    def test_9(self):
        """Here is test_9's doc str"""
        log.error('This is a failure case, which raises AssertionError')
        sleep(2)
        self.assertEqual(1, 2)

    @unittest.expectedFailure
    def test_10(self):
        """Here is test_10's doc str"""
        log.info('This is expected to be failed.')
        sleep(1)
        log.debug('Here is test_10 DEBUG log')
        raise ValueError


if __name__ == '__main__':
    # unittest loader will load test_5, test_6, test_7 for MyTestClass4 since it inherits MyTestClass3,
    # while unishark does not load test methods inherited from super class.
    # Try each of the following suites:
    # suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    # suite = unishark.DefaultTestLoader().load_tests_from_package('example', regex='test_module2\.\w+\.test\w*')
    suite = unishark.DefaultTestLoader().load_tests_from_modules(['example.test_module2'], regex='\w+4\.test\w*')
    reporter = unishark.HtmlReporter(dest='log')
    unishark.BufferedTestRunner(reporters=[reporter], verbosity=2).run(suite, name='mytest2', max_workers=2)
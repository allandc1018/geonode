from django.test.simple import DjangoTestSuiteRunner, TestCase
from django.test.simple import reorder_suite, build_test, build_suite
from django.db.models import get_app, get_apps
import unittest

class GeoNodeTestRunner(DjangoTestSuiteRunner):
    """ This test runner allows the exclusion of some
        of the apps from the test suite
    """
    EXCLUDED_APPS = [
        # Registration complains about email
        # messages in spanish, ticket has been filled at:
        # http://bitbucket.org/ubernostrum/django-registration/issue/93
                     'registration.models',
        # Django extensions tries to import keyczar to test the encryption
        # that import failing aborts the test suite run.
        # Keyczar test problems issue is being tracked at:
        # http://github.com/django-extensions/django-extensions/issues#issue/17  
                     'django_extensions.models']

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = unittest.TestSuite()

        if test_labels:
            for label in test_labels:
                if '.' in label:
                    suite.addTest(build_test(label))
                else:
                    app = get_app(label)
                    suite.addTest(build_suite(app))
        else:
            for app in get_apps():
                if app.__name__ not in self.EXCLUDED_APPS:
                    print app.__name__
                    suite.addTest(build_suite(app))

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (TestCase,))

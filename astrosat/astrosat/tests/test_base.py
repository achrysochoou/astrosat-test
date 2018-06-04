
__author__ = 'allyn.treshansky'

from django.db import connections, transaction
from django.db.models.query import QuerySet
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import CaptureQueriesContext
from unittest.util import safe_repr
from difflib import ndiff

import inspect
import os
import pprint

#############
# constants #
#############

# TEST_FILE_PATH = rel("tests/media")

# allows me to "trick" the test runner into thinking the test client sent an AJAX request
TEST_AJAX_REQUEST = {
    "HTTP_X_REQUESTED_WITH": "XMLHttpRequest",
}

##########################################
# a way of testing the number of queries #
# performed during an operation          #
##########################################


class QueryCounter(CaptureQueriesContext):
    """
    provides a context manager for me to keep track of the number of queries
    (not to be confused w/ assertNumQueries)

    usage is:
    >> test_query_counter = QueryCounter()
    >> with test_query_counter:
    >>     do_some_stuff()
    >>     test_query_count = test_query_counter.get_num_queries()
    """

    def __init__(self):
        conn = connections[DEFAULT_DB_ALIAS]
        super(QueryCounter, self).__init__(conn)

    def reset(self):
        self.initial_queries = 0
        self.final_queries = None

    def get_num_queries(self):
        try:
            num_queries = len(self.captured_queries)
            return num_queries
        except AttributeError:
            return 0


####################################
# a decorator for incomplete tests #
####################################

def incomplete_test(func):
    """
    decorator fn for incomplete tests
    :param func:
    :return:
    """
    def func_wrapper(self):
        msg = u'"{0}" is incomplete.'.format(func.__name__)
        raise NotImplementedError(msg)
    return func_wrapper


#########################
# the actual test class #
#########################

class AstrosatTestCase(TestCase):

    """
     The base class for all astrosat tests
     provides a reusable test client
     and some convenience fns for testing
    """

    maxDiff = None  # display full errors regardless of size
    # fixtures = ['testdata.json']  # using setUpTestData below instead of globally declaring fixtures here

    @classmethod
    def setUpTestData(cls):
        # load fixture data...
        call_command('loaddata', os.path.join(settings.BASE_DIR, "astrosat/fixtures/sites.json"), verbosity=0)

    def setUp(self):

        self.superuser = User.objects.create_superuser(
            username="admin",
            email="allyn.treshansky@gmail.com",
            password="password",
        )
        self.assertTrue(self.superuser.is_superuser)

        # factory is useful for creating simple requests
        self.factory = RequestFactory()
        # client is better-suited for most tests, though, b/c it has sessions, cookies, etc.
        self.client = Client()

    def tearDown(self):
        # this is for resetting things that are not db-related (ie: files, etc.)
        # but it's not needed for the db since each test is run in its own transaction
        pass

    ##############################
    # some additional assertions #
    ##############################

    def assertQuerysetEqual(self, qs1, qs2):
        """Tests that two django querysets are equal"""
        # the built-in TestCase method takes a qs and a list, which is confusing
        # this is more intuitive (see https://djangosnippets.org/snippets/2013/)

        pk = lambda o: o.pk
        return self.assertEqual(
            list(sorted(qs1, key=pk)),
            list(sorted(qs2, key=pk)),
        )

    def assertDictEqual(self, d1, d2, excluded_keys=[], **kwargs):
        """
        Overrides super.assertDictEqual fn to remove certain keys from either list before the comparison
        (uses "**kwargs" b/c sometimes this gets called by built-in Django fns)
        """

        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')

        d1_copy = d1.copy()
        d2_copy = d2.copy()
        for key_to_exclude in excluded_keys:
            d1_copy.pop(key_to_exclude, None)
            d2_copy.pop(key_to_exclude, None)

        msg = "{0} != {1}".format(safe_repr(d1_copy, True), safe_repr(d2_copy, True))
        diff = ('\n' + '\n'.join(ndiff(
            pprint.pformat(d1_copy).splitlines(),
            pprint.pformat(d2_copy).splitlines())))
        msg = self._truncateMessage(msg, diff)

        d1_keys = d1_copy.keys()
        d2_keys = d2_copy.keys()
        self.assertSetEqual(set(d1_keys), set(d2_keys), msg=msg)  # comparing as a set b/c order is irrelevant

        for key in d1_keys:
            d1_value = d1_copy[key]
            d2_value = d2_copy[key]
            # I am doing this instead of just calling super()
            # b/c Django doesn't consider querysets to be equal even if they point to the same thing
            # (see http://stackoverflow.com/questions/16058571/comparing-querysets-in-django-testcase)
            d1_type = type(d1_value)
            d2_type = type(d2_value)

            try:
                self.assertEqual(d1_type, d2_type, msg=msg)
            except AssertionError:
                # If I was checking strings & unicode objects or querysets & lists then the above assertion would have failed
                # so check those 2 special cases here...
                # string_types = [str, unicode, ]
                # if d1_type in string_types and d2_type in string_types:
                #     self.assertEqual(str(d1_value), str(d2_value))
                if QuerySet in inspect.getmro(d1_type) or QuerySet in inspect.getmro(d2_type): # lil bit of indirection here b/c custom managers acting as querysets might have been created dynamically
                    self.assertQuerysetEqual(d1_value, d2_value)
                else:
                    # ...and if it still fails, then go ahead and raise the original error
                    raise AssertionError(msg)


#################################################
# global fns to create static test content      #
# used when I just want to create these objects #
# w/out testing them                            #
#################################################

def create_facility(**kwargs):

    from astrosat.models.models_facilities import Facility

    _center = kwargs.pop("center")
    _facility = kwargs.pop("facility")
    _status = kwargs.pop("status", None)
    _facilityurl = kwargs.pop("facilityurl", None)
    _occupied = kwargs.pop("occupied", None)
    _center_search_status = kwargs.pop("center_search_status", None)
    _url_link = kwargs.pop("url_link", None)
    _record_date = kwargs.pop("record_date", None)
    _last_update = kwargs.pop("last_update", None)
    _country = kwargs.pop("country", None)
    _contact = kwargs.pop("contact", None)
    _phone = kwargs.pop("phone", None)
    #    location = models.Field
    _city = kwargs.pop("city", None)
    _state = kwargs.pop("state", None)
    _zipcode = kwargs.pop("zipcode", None)

    with transaction.atomic():
        facility = Facility(
            center=_center,
            facility=_facility,
        )

        if _status:
            facility.status = _status
        if _facilityurl:
            facility.facilityurl = _facilityurl
        if _occupied:
            facility.occupied = _occupied
        if _center_search_status:
            facility.center_search_status = _center_search_status
        if _url_link:
            facility.url_link = _url_link
        if _record_date:
            facility.record_date = _record_date
        if _last_update:
            facility.last_update = _last_update
        if _country:
            facility.country = _country
        if _contact:
            facility.contact = _contact
        if _phone:
            facility.phone = _phone
        if _city:
            facility.city = _city
        if _state:
            facility.state = _state
        if _zipcode:
            facility.zipcode = _zipcode

        facility.save()

    return facility


def remove_facility(**kwargs):

    facility = kwargs.pop("facility")
    facility.delete()

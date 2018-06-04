
__author__ = "allyn.treshansky"
"""
.. module:: test_context_processors

Tests for custom context_processors.
"""

from django.conf import settings
from django.urls import reverse

from astrosat.context_processors import *
from astrosat.tests.test_base import AstrosatTestCase


class Test(AstrosatTestCase):

    # def setUp(self):
    #     # no need for any questionnaire-specific stuff
    #     pass
    #
    # def tearDown(self):
    #     # no need for any questionnaire-specific stuff
    #     pass

    def test_debug(self):

        # just testing context_processors; don't need a _real_ request...
        test_context = self.client.get(reverse("test")).context

        self.assertEqual(settings.DEBUG, astrosat_debug(test_context).get("debug"))

    def test_cdn(self):

        # just testing context_processors; don't need a _real_ request...
        test_context = self.client.get(reverse("test")).context

        self.assertEqual(settings.CDN, astrosat_cdn(test_context).get("cdn"))



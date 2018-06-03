"""
.. module:: models_sites

"""

from enum import Enum

from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings

from astrosat import APP_LABEL
from astrosat.constants import *


class AstrosatSiteTypes(Enum):
    LOCAL = 1  # auto()
    TEST = 2  # auto()
    DEV = 3  # auto()
    PROD = 4  # auto()


class AstrosatSite(models.Model):

    class Meta:
        app_label = APP_LABEL
        abstract = False
        verbose_name = 'Astrosat Site'
        verbose_name_plural = 'Astrosat Sites'

    # 1to1 relationship w/ standard Django Site...
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="astrosat_site")

    # extra info associated w/ a Tings Site...
    type = models.CharField(
        max_length=LIL_STRING,
        blank=True,
        choices=[(t.name, t.name) for t in AstrosatSiteTypes]
    )

    def __str__(self):
        return "{0}".format(self.site)

    @classmethod
    def get_current_site(self):
        # assuming that requests have been made prior to calling this fn,
        # the "dynamic_sites" middleware will have run which will have set "settings.SITE_ID" correctly
        return Site.objects.get(pk=settings.SITE_ID)

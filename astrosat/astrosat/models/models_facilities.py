from django.db import models
from .models_base import AstrosatModel
from astrosat import APP_LABEL

from astrosat.constants import *


class FacilityQuerySet(models.QuerySet):

    """
    A simple QS manager for Facilities
    allows me to intuitively filter on active/inactive facilities
    """

    def active(self):
        return self.filter(status="Active")

    def inactive(self):
        return self.exclude(is_registered=True)


class Facility(AstrosatModel):
    """
    A facility
    All these fields come directly from the NASA API
    A facility is uniquely identified by its "center" and "facility" fields
    """
    class Meta:
        app_label = APP_LABEL
        abstract = False
        verbose_name = "NASA Facility"
        verbose_name_plural = "NASA Facilities"
        unique_together = ("center", "facility")

    objects = FacilityQuerySet.as_manager()

    center = models.CharField(verbose_name="Center", max_length=SMALL_STRING)
    center_search_status = models.CharField(verbose_name="Center Search Status", max_length=SMALL_STRING)
    facility = models.CharField(verbose_name="Facility", max_length=SMALL_STRING)
    facilityurl = models.URLField(verbose_name="FacilityURL")
    occupied = models.DateTimeField(verbose_name="Occupied", null=True)
    status = models.CharField(verbose_name="status", max_length=SMALL_STRING)
    url_link = models.URLField(verbose_name="URL Link")
    record_date = models.DateTimeField(verbose_name="Record Date", null=True)
    last_update = models.DateTimeField(verbose_name="Last Update", null=True)
    country = models.CharField(verbose_name="Country", max_length=SMALL_STRING)
    contact = models.CharField(verbose_name="Contact", max_length=SMALL_STRING)
    phone = models.CharField(verbose_name="Phone", max_length=SMALL_STRING)
    # TODO: WHAT THE HELL IS A LOCATION FIELD?
#    location = models.Field
    city = models.CharField(verbose_name="City", max_length=SMALL_STRING)
    state = models.CharField(verbose_name="State", max_length=SMALL_STRING)
    zipcode = models.CharField(verbose_name="Zipcode", max_length=SMALL_STRING)

    def __str__(self):
        """
        A pretty way of printing a facility
        :return:
        """
        return "{0}: {1}".format(self.center, self.facility)

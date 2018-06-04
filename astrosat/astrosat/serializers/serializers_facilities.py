from rest_framework import serializers
from astrosat.models.models_facilities import Facility


class FacilitySerializer(serializers.ModelSerializer):
    """
    Django-Rest-Framework for Facilities
    Does nothing fancy, just includes all the fields
    """

    class Meta:
        model = Facility
        fields = (
            'id',
            'center',
            'center_search_status',
            'facility',
            'facilityurl',
            'occupied',
            'status',
            'url_link',
            'record_date',
            'last_update',
            'country',
            'contact',
            'phone',
            # 'location',
            'city',
            'state',
            'zipcode',
        )

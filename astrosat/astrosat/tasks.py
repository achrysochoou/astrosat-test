from celery import shared_task

import requests
from requests.exceptions import RequestException

from astrosat.models.models_facilities import Facility
from astrosat.serializers.serializers_facilities import FacilitySerializer
from astrosat.constants import NASA_FACILITIES_URL


@shared_task
def import_facilities():
    try:
        response = requests.get(NASA_FACILITIES_URL)
        contents = response.json()
    except RequestException as e:
        pass

    for content in contents:
        facility_center = content.pop("center")
        facility_name = content.pop("facility")

        facility, created = Facility.objects.get_or_create(center=facility_center, facility=facility_name)

        if created:
            valid_fields = {
                k: v
                for k, v in content.items()
                if facility.get_field(k) is not None
            }

            facility_serializer = FacilitySerializer()
            facility_serializer.update(instance=facility, validated_data=valid_fields)

    return contents

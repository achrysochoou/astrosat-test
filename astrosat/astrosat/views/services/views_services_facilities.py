from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from astrosat.models.models_facilities import Facility
from astrosat.serializers.serializers_facilities import FacilitySerializer
from astrosat.tasks import import_facilities


VALID_METHODS = ["POST"]


def import_facilities_now(request):

    if not request.is_ajax():
        return HttpResponseForbidden("Attempt to call service outside of AJAX.")
    if request.method not in VALID_METHODS:
        return HttpResponseForbidden("Attempt to call service with '{0}' method.".format(request.method))

    try:
        # obviously the point of celery is to do these tasks asynchronously
        # but if you run it manually via this service, I kind of feel like it's okay to wait for ".get()" to finish
        async_result = import_facilities.delay()
        return JsonResponse(async_result.get(), safe=False)
        # active_facilities = Facility.objects.active()
        # serializer = FacilitySerializer(active_facilities, many=True)
        # return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(e)

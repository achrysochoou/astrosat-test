from .views_api_facilities import FacilityViewSet
from .views_api_tasks import TaskResultViewSet

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'facilities': reverse('facilities-list', request=request, format=format),
        'tasks': reverse('tasks-list', request=request, format=format),
    })

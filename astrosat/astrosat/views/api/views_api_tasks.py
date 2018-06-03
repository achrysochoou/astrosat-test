from rest_framework import viewsets

from django_celery_results.models import TaskResult
from astrosat.serializers import TaskResultSerializer


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = TaskResultSerializer
    queryset = TaskResult.objects.filter(status="SUCCESS").order_by("-date_done")

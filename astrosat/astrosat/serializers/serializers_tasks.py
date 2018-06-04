from rest_framework import serializers
from django_celery_results.models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    """
    Django-Rest-Framework serializer for Tasks
    I use django_celery_results to store celery tasks in the Django DB
    this makes them easy to play with in code (they're just another Django Model)
    I include all fields except for the "result" field which can potentially have loads of JSON and slow things down
    """
    class Meta:
        model = TaskResult
        fields = (
            'id',
            'task_id',
            'status',
            'content_type',
            'content_encoding',
            # 'result',
            'date_done',
        )

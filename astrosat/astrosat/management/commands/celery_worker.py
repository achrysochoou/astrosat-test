from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import subprocess

from astrosat import APP_LABEL


class Command(BaseCommand):

    help = "Convenience function for running celery for the {0} app".format(APP_LABEL)

    def handle(self, *args, **options):
        # note that this runs in both "worker" & "beat" mode
        # this allows me to run tasks via the beat scheduler (automatically)
        # and run tasks as desired using services via the normal worker scheduler (manually)
        cmd = "celery -A {0} worker --beat -l info --scheduler django".format(APP_LABEL)
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, cwd=settings.BASE_DIR)
        # self.stdout.write(self.style.SUCCESS(proc.stdout))

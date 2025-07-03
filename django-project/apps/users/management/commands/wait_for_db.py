import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Waits for the database to be available.'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        max_attempts = 60  # Adjust as needed (e.g., 60 seconds)

        for _ in range(max_attempts):
            try:
                db_conn = connections['default'].cursor()
                break  # Database is ready
            except OperationalError:
                time.sleep(1)  # Wait for 1 second
        if db_conn:
            self.stdout.write(self.style.SUCCESS('Database is ready!'))
        else:
            self.stdout.write(self.style.ERROR('Database is not available after multiple attempts.'))
            exit(1) # Exit with an error code if the database is not available

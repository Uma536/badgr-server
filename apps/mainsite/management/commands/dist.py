import os
from subprocess import call

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Runs build tasks to compile javascript and css'

    def handle(self, *args, **options):
        """
        Builds gulp resources.
        Gulp must be installed, and node_modules must be populated with `npm install`
        """

        if apps.is_installed('badgebook'):
            # if badgebook is present, build its grunt
            import pkg_resources
            gruntfile_path = pkg_resources.resource_filename('badgebook', 'Gruntfile.js')
            badgebook_dir = os.path.dirname(gruntfile_path)
            ret = call(['npm', 'install'], cwd=badgebook_dir)
            if ret != 0:
                raise CommandError("badgebook npm install failed")

            ret = call(['grunt', '--gruntfile', gruntfile_path, 'dist'])
            if ret != 0:
                raise CommandError("badgebook grunt dist failed")

        ret = call(['grunt', 'dist'])
        if ret != 0:
            raise CommandError("grunt dist failed")
        #management.call_command('test', verbosity=1)

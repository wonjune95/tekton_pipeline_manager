import os
import sys

from django.core.management import execute_from_command_line

# ok: mois-6-02-debug-code-py Django 관리 명령 시작 블록
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")
    execute_from_command_line(sys.argv)

#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    if (os.getenv('PLATFORM_APPLICATION_NAME') is None):
        if (os.getenv('CVBACK_PRODUCTION') == 'True'):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.platform")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # cvback directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "cvback"))

    execute_from_command_line(sys.argv)
